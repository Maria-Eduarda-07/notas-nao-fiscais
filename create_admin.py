from app import create_app
from models import db, User

app = create_app()
with app.app_context():
    username = input("Usuário admin: ").strip()
    password = input("Senha admin: ").strip()
    u = User(username=username, is_admin=True)
    u.set_password(password)
    db.session.add(u)
    db.session.commit()
    print("Admin criado:", username)
