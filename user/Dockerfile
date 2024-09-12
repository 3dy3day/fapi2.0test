FROM python:3.10-slim

WORKDIR /app

# Install OpenSSL
RUN apt-get update && apt-get install -y openssl && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . .

# Copy requirements and install dependencies
RUN pip install -r requirements.txt

# Run certs script
RUN chmod +x /app/generate-cert.sh
RUN sh /app/generate-cert.sh

CMD ["python", "client.py"]
