#!/bin/bash

mkdir -p /app/certs

# Generate User certificate and private key for ES256
openssl ecparam -genkey -name prime256v1 -noout -out /app/certs/user.key
openssl req -new -x509 -key /app/certs/user.key -out /app/certs/user.crt -days 365 -subj "/CN=user"