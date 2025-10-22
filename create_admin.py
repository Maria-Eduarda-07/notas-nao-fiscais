# create_admin.py
import os
from app import app, db
from models import User

# Configurações do admin
USERNAME = "admin"
PASSWORD = "123456"

with app.app_context():
    # Verifica se o admin já existe
    if User.query.filter_by(username=USERNAME).first():
        print(f"✅ Usuário '{USERNAME}' já existe!")
    else:
        # Cria novo usuário admin
        admin = User(username=USERNAME)
        admin.set_password(PASSWORD)  # garante hash correto
        db.session.add(admin)
        db.session.commit()
        print(f"✅ Usuário admin '{USERNAME}' criado com sucesso!")

