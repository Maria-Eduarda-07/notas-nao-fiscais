from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco_unit = db.Column(db.Numeric(10, 2))

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=True)
    tipo = db.Column(db.String(50), nullable=False)  # fiscal ou não fiscal
    data = db.Column(db.DateTime, default=datetime.utcnow)

class InvoiceItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)
    descricao = db.Column(db.String(200))
    preco_unit = db.Column(db.Numeric(10, 2))
