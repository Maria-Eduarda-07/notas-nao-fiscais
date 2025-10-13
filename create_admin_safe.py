from werkzeug.security import generate_password_hash
from app import app, db
from models import User

# Configurações do admin
username = "admin"
password = "admin123"  # Troque aqui para a senha que você quer
# email não é obrigatório, então podemos omitir se a tabela não tiver

with app.app_context():
    # Verifica se já existe
    admin = User.query.filter_by(username=username).first()
    if admin:
        print(f"✅ Usuário '{username}' já existe.")
    else:
        # Cria o admin
        admin = User(username=username)
        admin.set_password(password)  # usa método do modelo
        db.session.add(admin)
        db.session.commit()
        print(f"✅ Usuário admin '{username}' criado com sucesso!")

