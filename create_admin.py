from app import app, db
from models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    username = "admin"
    email = "admin@admin.com"
    password = "123456"

    # verifica se já existe
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        print("✅ Usuário admin já existe!")
    else:
        admin = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )
        db.session.add(admin)
        db.session.commit()
        print("🎉 Usuário admin criado com sucesso!")
