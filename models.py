from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    cpf_cnpj = db.Column(db.String(40))
    endereco = db.Column(db.String(400))
    email = db.Column(db.String(200))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    preco_unit = db.Column(db.Numeric(12,2), nullable=False, default=0)
    estoque = db.Column(db.Integer, default=0)

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(64), nullable=False, unique=True)
    tipo = db.Column(db.String(20), nullable=False)  # 'fiscal' ou 'nao_fiscal'
    cliente_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=True)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Numeric(14,2), default=0)
    xml = db.Column(db.Text)  # para armazenar XML/NFE se integrar
    cliente = db.relationship('Client', backref='invoices')
    itens = db.relationship('InvoiceItem', backref='invoice', cascade='all, delete-orphan', lazy=True)

class InvoiceItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)
    descricao = db.Column(db.String(300))
    quantidade = db.Column(db.Integer, default=1)
    preco_unit = db.Column(db.Numeric(12,2), default=0)

