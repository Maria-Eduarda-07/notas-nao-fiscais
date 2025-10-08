# config.py
class Config:
    DEBUG = True
    SECRET_KEY = 'bob_esponja'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///notas.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

