from flask import Flask, jsonify, request
import jwt
from jose import jws
import requests
import os

app = Flask(__name__)

# Account storage (for demo purposes)
accounts = {'user1': {'balance': 10000}}

# IDP URL to fetch the public key
IDP_URL = "http://idp:9000"

# Fetch the public key from the IDP
def fetch_public_key():
    response = requests.get(f"{IDP_URL}/public_key")
    if response.status_code == 200:
        return response.text
    else:
        raise Exception("Failed to fetch public key from IDP")

# JWT Public key for verification
PUBLIC_KEY = fetch_public_key()

# Utility to verify the JWT token
def verify_token(token):
    try:
        decoded = jwt.decode(token, PUBLIC_KEY, algorithms=["ES256"])
        return decoded
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@app.route('/account', methods=['GET'])
def get_account_info():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "Unauthorized"}), 401
    
    token = auth_header.split(" ")[1]
    user_data = verify_token(token)
    if not user_data:
        return jsonify({"error": "Invalid token"}), 403
    
    user_id = user_data['clientId']
    if user_id in accounts:
        account_info = {
            "account_id": user_id,
            "balance": accounts[user_id]['balance'],
            "currency": "USD"
        }

        # Sign the response using JWS
        signed_response = jws.sign(account_info, 'secret', algorithm='HS256')
        return jsonify({"signed_response": signed_response})
    else:
        return jsonify({"error": "Account not found"}), 404

@app.route('/deposit', methods=['POST'])
def deposit():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "Unauthorized"}), 401
    
    token = auth_header.split(" ")[1]
    user_data = verify_token(token)
    if not user_data:
        return jsonify({"error": "Invalid token"}), 403
    
    user_id = user_data['clientId']
    amount = request.json.get('amount')
    if user_id in accounts:
        accounts[user_id]['balance'] += amount
        return jsonify({"newBalance": accounts[user_id]['balance']})
    else:
        return jsonify({"error": "Account not found"}), 404

@app.route('/withdraw', methods=['POST'])
def withdraw():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "Unauthorized"}), 401
    
    token = auth_header.split(" ")[1]
    user_data = verify_token(token)
    if not user_data:
        return jsonify({"error": "Invalid token"}), 403
    
    user_id = user_data['clientId']
    amount = request.json.get('amount')
    if user_id in accounts:
        if accounts[user_id]['balance'] >= amount:
            accounts[user_id]['balance'] -= amount
            return jsonify({"newBalance": accounts[user_id]['balance']})
        else:
            return jsonify({"error": "Insufficient funds"}), 400
    else:
        return jsonify({"error": "Account not found"}), 404

@app.route('/public_cert', methods=['GET'])
def public_cert():
    cert_path = os.path.join('/app/certs', 'bank.crt')
    with open(cert_path, 'r') as f:
        cert = f.read()
    return cert

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, ssl_context=('/app/certs/bank.crt', '/app/certs/bank.key'))
