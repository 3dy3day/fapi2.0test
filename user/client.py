import requests

IDP_URL = "http://localhost:9000"
BANK_API_URL = "https://localhost:8000"

# Login function to authenticate the user
def login(username, password):
    response = requests.post(f"{IDP_URL}/login", json={
        "username": username,
        "password": password
    })

    if response.status_code == 200:
        return response.json()["token"]
    else:
        raise Exception("Login failed: " + response.json()["error"])

# Deposit money
def deposit(token, amount):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BANK_API_URL}/deposit", json={"amount": amount}, headers=headers)
    if response.status_code == 200:
        print(f"Deposit successful. New balance: {response.json()['newBalance']}")
    else:
        print("Deposit failed: " + response.json()["error"])

# Withdraw money
def withdraw(token, amount):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BANK_API_URL}/withdraw", json={"amount": amount}, headers=headers)
    if response.status_code == 200:
        print(f"Withdrawal successful. New balance: {response.json()['newBalance']}")
    else:
        print("Withdrawal failed: " + response.json()["error"])

# Get account balance
def get_account_info(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BANK_API_URL}/account", headers=headers)
    if response.status_code == 200:
        print(f"Account Info: {response.json()}")
    else:
        print("Failed to get account info: " + response.json()["error"])

# Logout
def logout(token):
    response = requests.post(f"{IDP_URL}/logout", json={"token": token})
    if response.status_code == 200:
        print("Logout successful")
    else:
        print("Logout failed: " + response.json()["error"])

if __name__ == '__main__':
    print("Starting Client")
    token = login("user1", "password1")
    deposit(token, 2000)
    withdraw(token, 5000)
    get_account_info(token)
    logout(token)
    print("Ending Client")
