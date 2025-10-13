# create_admin.py
from app import create_app, db
from models import User

# 🔥 Configura o app e contexto
app = create_app()

with app.app_context():
    # Dados do admin
    username = "admin"
    senha = "123456"  # altere para sua senha segura

    # Verifica se o admin já existe
    if User.query.filter_by(username=username).first():
        print(f"Usuário '{username}' já existe!")
    else:
        # Cria o admin
        admin = User(username=username)
        admin.password = senha  # usa o setter do modelo para gerar password_hash

        db.session.add(admin)
        db.session.commit()
        print(f"Usuário admin '{username}' criado com sucesso!")
