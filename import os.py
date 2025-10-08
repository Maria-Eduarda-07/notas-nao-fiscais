import os
from dotenv import load_dotenv
load_dotenv()

class config:
    SECRET_KEY = os.getenv('SECRET_KEY', "mudar_essa_chave")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", 'sqlite:///notas,db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    NFEIO_API_KEY = os.getenv("NFEIO_API_KEY") #placeholder
