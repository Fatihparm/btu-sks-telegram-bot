FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

VOLUME ["/app/database.db"]

EXPOSE 8080

COPY .env .env

CMD ["python", "main.py"]
