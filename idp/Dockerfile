FROM node:18-alpine

WORKDIR /app


COPY ../certs/generate_certs.sh /app/generate_certs.sh

COPY package.json package-lock.json /app/
RUN npm install

RUN chmod +x /app/generate_certs.sh && /app/generate_certs.sh

COPY . .

CMD ["npm", "start"]
