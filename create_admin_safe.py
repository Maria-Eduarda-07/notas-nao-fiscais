from werkzeug.security import generate_password_hash
from app import app, db, User  # importando app diretamente

# Dados do admin
username = "admin"
password = "admin123"

with app.app_context():  # ✅ usar o app aqui, não db.app
    existing = User.query.filter_by(username=username).first()
    if existing:
        print(f"✅ Usuário '{username}' já existe. Nada foi criado.")
    else:
        admin = User(username=username, password_hash=generate_password_hash(password))
        db.session.add(admin)
        db.session.commit()
        print(f"✅ Usuário admin '{username}' criado com sucesso!")

