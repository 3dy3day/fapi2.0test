import requests
import jwt
import time
import uuid

IDP_URL = "http://idp:9000"
BANK_API_URL = "https://bank:8000"

# Fetch the Bank's public certificate
def fetch_bank_cert():
    response = requests.get(f"{BANK_API_URL}/public_cert")
    if response.status_code == 200:
        with open("/app/certs/bank.crt", "w") as f:
            f.write(response.text)
    else:
        raise Exception("Failed to fetch Bank's public certificate")

# Generate DPoP header
def generate_dpop_header(url, method, private_key):
    jti = str(uuid.uuid4())
    iat = int(time.time())
    dpop_payload = {
        "htu": url,
        "htm": method,
        "jti": jti,
        "iat": iat
    }
    dpop_token = jwt.encode(dpop_payload, private_key, algorithm="ES256")
    return dpop_token

# Login function to authenticate the user
def login(username, password):
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(f"{IDP_URL}/login", json={
        "username": username,
        "password": password
    }, headers=headers)

    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.content}")

    if response.status_code == 200:
        return response.json()["token"]
    else:
        raise Exception("Login failed: " + response.json()["error"])

# Deposit money
def deposit(token, amount, private_key):
    headers = {
        "Authorization": f"Bearer {token}",
        "DPoP": generate_dpop_header(f"{BANK_API_URL}/deposit", "POST", private_key),
        "Content-Type": "application/json"
    }
    response = requests.post(f"{BANK_API_URL}/deposit", json={"amount": amount}, headers=headers, verify='/app/certs/bank.crt')
    if response.status_code == 200:
        print(f"Deposit successful. New balance: {response.json()['newBalance']}")
    else:
        print("Deposit failed: " + response.json()["error"])

# Withdraw money
def withdraw(token, amount, private_key):
    headers = {
        "Authorization": f"Bearer {token}",
        "DPoP": generate_dpop_header(f"{BANK_API_URL}/withdraw", "POST", private_key),
        "Content-Type": "application/json"
    }
    response = requests.post(f"{BANK_API_URL}/withdraw", json={"amount": amount}, headers=headers, verify='/app/certs/bank.crt')
    if response.status_code == 200:
        print(f"Withdrawal successful. New balance: {response.json()['newBalance']}")
    else:
        print("Withdrawal failed: " + response.json()["error"])

# Get account balance
def balance(token, private_key):
    headers = {
        "Authorization": f"Bearer {token}",
        "DPoP": generate_dpop_header(f"{BANK_API_URL}/account", "GET", private_key),
        "Content-Type": "application/json"
    }
    response = requests.get(f"{BANK_API_URL}/account", headers=headers, verify='/app/certs/bank.crt')
    if response.status_code == 200:
        print(f"Account Info: {response.json()}")
    else:
        print("Failed to get account info: " + response.json()["error"])

# Logout
def logout(token):
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(f"{IDP_URL}/logout", json={"token": token}, headers=headers)
    if response.status_code == 200:
        print("Logout successful")
    else:
        print("Logout failed: " + response.json()["error"])

if __name__ == '__main__':
    print("Starting Client")
    fetch_bank_cert()  # Fetch the Bank's public certificate
    private_key = open("/app/certs/user.key").read()
    token = login("user1", "password1")
    deposit(token, 2000, private_key)
    # withdraw(token, 5000, private_key)
    # balance(token, private_key)
    logout(token)
    print("Ending Client")
