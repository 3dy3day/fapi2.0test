#!/bin/bash

mkdir -p /app/certs

# Generate Bank certificate and private key for ES256
openssl ecparam -genkey -name prime256v1 -noout -out /app/certs/bank.key
openssl req -new -x509 -key /app/certs/bank.key -out /app/certs/bank.crt -days 365 -subj "/CN=bank"