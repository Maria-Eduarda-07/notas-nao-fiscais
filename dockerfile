FROM python:3.11-slim

# instalar dependências do sistema para weasyprint
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libcairo2 \
    libpango-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libpangocairo-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV FLASK_ENV=production
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080", "--workers", "2"]
