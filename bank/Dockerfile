FROM python:3.10-slim

WORKDIR /app

COPY ../certs/generate_certs.sh /app/generate_certs.sh

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN chmod +x /app/generate_certs.sh && /app/generate_certs.sh

COPY . .

CMD ["python", "bank_api.py"]
