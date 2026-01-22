FROM python:3.11-slim

WORKDIR /app

# Evita .pyc y fuerza logs inmediatos
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código
COPY . .

EXPOSE 5001

# Ajusta el comando según tu entrypoint real
CMD ["python", "run.py"]
