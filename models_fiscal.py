# models_fiscal.py
from datetime import datetime
from models import db

# --------------------------- EMITENTE ---------------------------
class Emitente(db.Model):
    __tablename__ = "emitente"
    id = db.Column(db.Integer, primary_key=True)
    razao_social = db.Column(db.String(120), nullable=False)
    nome_fantasia = db.Column(db.String(120))
    cnpj = db.Column(db.String(14), unique=True, nullable=False)
    ie = db.Column(db.String(20))
    uf = db.Column(db.String(2))
    municipio = db.Column(db.String(60))
    logradouro = db.Column(db.String(255))
    numero = db.Column(db.String(20))
    cep = db.Column(db.String(8))
    certificado_a1_path = db.Column(db.String(255))  # caminho do .pfx
    senha_certificado = db.Column(db.String(255))
    ambiente = db.Column(db.String(20), default="homologacao")  # homologacao ou producao
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

# --------------------------- DESTINATÁRIO ---------------------------
class Destinatario(db.Model):
    __tablename__ = "destinatario"
    id = db.Column(db.Integer, primary_key=True)
    cpf_cnpj = db.Column(db.String(14))
    razao_social = db.Column(db.String(120))
    email = db.Column(db.String(120))
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(255))
    municipio = db.Column(db.String(60))
    uf = db.Column(db.String(2))

# --------------------------- NOTA FISCAL ---------------------------
class NotaFiscal(db.Model):
    __tablename__ = "nota_fiscal"
    id = db.Column(db.Integer, primary_key=True)
    emitente_id = db.Column(db.Integer, db.ForeignKey("emitente.id"))
    destinatario_id = db.Column(db.Integer, db.ForeignKey("destinatario.id"))
    modelo = db.Column(db.String(2), default="55")  # 55 = NF-e / 65 = NFC-e
    serie = db.Column(db.String(3), default="1")
    numero = db.Column(db.Integer)
    data_emissao = db.Column(db.DateTime, default=datetime.utcnow)
    valor_total = db.Column(db.Numeric(12, 2))
    status = db.Column(db.String(50), default="Em Digitação")
    chave_acesso = db.Column(db.String(44))
    xml_path = db.Column(db.String(255))  # caminho do XML gerado
    pdf_path = db.Column(db.String(255))  # caminho do DANFE
    data_autorizacao = db.Column(db.DateTime)

# --------------------------- ITENS DA NOTA ---------------------------
class NotaItem(db.Model):
    __tablename__ = "nota_item"
    id = db.Column(db.Integer, primary_key=True)
    nota_id = db.Column(db.Integer, db.ForeignKey("nota_fiscal.id"))
    descricao = db.Column(db.String(255))
    quantidade = db.Column(db.Numeric(10, 3))
    valor_unitario = db.Column(db.Numeric(10, 2))
    ncm = db.Column(db.String(8))
    cfop = db.Column(db.String(4))
    cst = db.Column(db.String(3))
    aliquota_icms = db.Column(db.Numeric(5, 2))
    total = db.Column(db.Numeric(10, 2))
