import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "eduarda256")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///notas.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email (opcional) para envio de nota por email
    SMTP_HOST = os.environ.get("SMTP_HOST")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
    SMTP_USER = os.environ.get("SMTP_USER")
    SMTP_PASS = os.environ.get("SMTP_PASS")
    FROM_EMAIL = os.environ.get("FROM_EMAIL")


