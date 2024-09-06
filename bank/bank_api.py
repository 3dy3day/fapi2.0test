from flask import Flask, jsonify, request
import jwt
from jose import jws

app = Flask(__name__)

# Account storage (for demo purposes)
accounts = {'user1': {'balance': 10000}}

# JWT Public key for verification
PUBLIC_KEY = open("/certs/server.crt").read()

# Utility to verify the JWT token
def verify_token(token):
    try:
        decoded = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, ssl_context=('/certs/server.crt', '/certs/server.key'))
