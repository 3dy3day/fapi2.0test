# FAPI 2.0 Test Implementation

This project simulates a Financial-grade API (FAPI) 2.0 compliant system, including an Identity Provider (IDP), a Bank API, and a User Client. It includes features such as Pushed Authorization Requests (PAR), Demonstration of Proof of Possession (DPoP), and Message Signing (JWS).

## Setup

### Prerequisites

- Docker and Docker Compose must be installed.

### Steps to Set Up

1. Clone the repository:
```bash
git clone https://github.com/your-repo/fapi_simulation.git
cd fapi_simulation
```

2. Build and start the services:
```bash
docker-compose up --build
```

3. The following services will be available:
- **IDP**: http://localhost:9000
- **Bank API**: https://localhost:8000

## Transaction Flow

### Scenario
1. **Login**: The user logs in to receive an access token.
2. **Deposit**: The user deposits $2,000 into their bank account.
3. **Withdraw**: The user withdraws $5,000 from the account.
4. **Check Balance**: The user retrieves the current account balance.
5. **Logout**: The user logs out and invalidates their token.

### Communication
- **Login**: The client sends login credentials to the IDP and retrieves a JWT token.
- **PAR**: The client pushes the authorization request to the IDP via the PAR endpoint.
- **DPoP**: The client proves possession of the token with DPoP when accessing the Bank API.
- **JWS**: The Bank API signs responses using JWS for message integrity.

## Verifying Transactions
1. View Transaction Logs: The IDP logs all transactions. To view the logs:
```bash
curl http://localhost:9000/transactions

```
2. Simulate **Operations****: Use the client to deposit/withdraw and check the balance to verify the system's behavior.

## Example Requests

### Login
```bash
curl -X POST http://localhost:9000/login -H "Content-Type: application/json" -d '{
  "username": "user1",
  "password": "password1"
}'

```

### Deposit
```bash
curl -X POST https://localhost:8000/deposit -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{
  "amount": 2000
}'

```

### Withdraw
```bash
curl -X POST https://localhost:8000/withdraw -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{
  "amount": 5000
}'

```

### Check Account Balance
```bash
curl -X GET https://localhost:8000/account -H "Authorization: Bearer <token>"

```

### Logout
```bash
curl -X POST http://localhost:9000/logout -H "Content-Type: application/json" -d '{
  "token": "<token>"
}'

```
