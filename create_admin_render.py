from app import app, db
from models import User

with app.app_context():
    username = "admin"
    password = "admin123"

    admin = User.query.filter_by(username=username).first()
    if admin:
        print(f"⚠️ Usuário '{username}' já existe no banco do Render.")
    else:
        admin = User(username=username)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print(f"✅ Usuário admin criado com sucesso! ({username}/{password})")
