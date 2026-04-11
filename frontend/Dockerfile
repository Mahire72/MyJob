FROM python:3.11-slim

WORKDIR /app

COPY . .

EXPOSE 80

CMD ["python", "-m", "http.server", "80", "--bind", "0.0.0.0"]
