#!/bin/bash

mkdir -p /app/certs

# Generate IDP certificate and private key for ES256
openssl ecparam -genkey -name prime256v1 -noout -out /app/certs/idp.key
openssl req -new -x509 -key /app/certs/idp.key -out /app/certs/idp.crt -days 365 -subj "/CN=idp"