#!/bin/bash

# Server Cert
openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 \
  -keyout /certs/server.key -out /certs/server.crt -subj "/CN=localhost"

# Client Cert
openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 \
  -keyout /certs/client.key -out /certs/client.crt -subj "/CN=client"
