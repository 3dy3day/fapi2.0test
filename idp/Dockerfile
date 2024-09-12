FROM node:18-alpine

WORKDIR /app

# Install OpenSSL
RUN apk add --no-cache openssl

# Copy application code
COPY . .

# Run certs script
RUN chmod +x /app/generate-cert.sh
RUN sh /app/generate-cert.sh

# Install dependencies
RUN npm install
RUN npm run build

CMD ["npm", "start"]
