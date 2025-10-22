from app import app
from models import db, User
import sqlite3
import os


def ensure_is_admin_column(app):
    uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    # suporta URIs do tipo sqlite:///notas.db ou sqlite:////abs/path
    if uri.startswith('sqlite:///'):
        db_path = uri.replace('sqlite:///', '', 1)
    elif uri.startswith('sqlite:////'):
        db_path = '/' + uri.replace('sqlite:////', '', 1)
    else:
        # fallback para arquivo local chamado notas.db
        db_path = 'notas.db'

    # Certifica que o caminho é relativo ao diretório do projeto
    db_path = os.path.abspath(db_path)
    if not os.path.exists(db_path):
        return

    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(user);")
        cols = [r[1] for r in cur.fetchall()]
        if 'is_admin' not in cols:
            cur.execute("ALTER TABLE user ADD COLUMN is_admin BOOLEAN DEFAULT 0")
            conn.commit()
    finally:
        conn.close()


# Inicializa o contexto do app
with app.app_context():
    # garante que a coluna is_admin exista na tabela
    ensure_is_admin_column(app)

    username = input("Usuário admin: ")
    senha = input("Senha admin: ")

    # evita criar usuário duplicado
    existing = User.query.filter_by(username=username).first()
    if existing:
        print(f"Usuário '{username}' já existe.")
    else:
        # Cria o usuário admin
        admin = User(username=username)
        admin.set_password(senha)  # se você tiver função de hash
        admin.is_admin = True
        db.session.add(admin)
        db.session.commit()

        print(f"Admin criado: {username}")

