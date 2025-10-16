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

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    cpf_cnpj = db.Column(db.String(20))
    endereco = db.Column(db.String(300))
    uf = db.Column(db.String(2))
    telefone = db.Column(db.String(30))
    email = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    notas = db.relationship('Nota', backref='destinatario', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    preco_unit = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    estoque = db.Column(db.Integer, default=0)

class Nota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chave_acesso = db.Column(db.String(44), unique=True, nullable=True)
    modelo = db.Column(db.String(2), default="55")  # 55 NF-e, 65 NFC-e
    serie = db.Column(db.String(10), default="1")
    numero = db.Column(db.Integer)
    data_emissao = db.Column(db.DateTime, default=datetime.utcnow)
    emitente_cnpj = db.Column(db.String(20))
    destinatario_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    valor_total = db.Column(db.Numeric(12, 2))
    status = db.Column(db.String(30), default="rascunho")  # rascunho, emitida, cancelada
    itens = db.relationship('NotaItem', backref='nota', cascade="all, delete-orphan", lazy=True)

class NotaItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nota_id = db.Column(db.Integer, db.ForeignKey('nota.id'))
    descricao = db.Column(db.String(300))
    ncm = db.Column(db.String(10))
    cfop = db.Column(db.String(10))
    quantidade = db.Column(db.Numeric(12, 4))
    unidade = db.Column(db.String(10))
    valor_unitario = db.Column(db.Numeric(12, 2))
    icms_aliquota = db.Column(db.Numeric(5, 2))

    @property
    def subtotal(self):
        return self.quantidade * self.valor_unitario
