from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class NotaNaoFiscal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, unique=True, nullable=False)
    cliente_nome = db.Column(db.String(120), nullable=False)
    cliente_cpf = db.Column(db.String(14), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    data_emissao = db.Column(db.DateTime, default=datetime.utcnow)
