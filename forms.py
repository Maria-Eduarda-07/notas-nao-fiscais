from flask_wtf import FlaskForm
from wtforms import (
    StringField, DecimalField, IntegerField, SubmitField,
    SelectField, PasswordField, HiddenField
)
from wtforms.validators import DataRequired, Optional

class LoginForm(FlaskForm):
    username = StringField("Usuário", validators=[DataRequired()])
    password = PasswordField("Senha", validators=[DataRequired()])
    submit = SubmitField("Entrar")

class ClientForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
    cpf_cnpj = StringField("CPF/CNPJ", validators=[Optional()])
    endereco = StringField("Endereço", validators=[Optional()])
    uf = StringField("UF", validators=[Optional()])
    telefone = StringField("Telefone", validators=[Optional()])
    email = StringField("E-mail", validators=[Optional()])
    submit = SubmitField("Salvar")

class ProductForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
    preco_unit = DecimalField("Preço", validators=[DataRequired()])
    estoque = IntegerField("Estoque", validators=[Optional()])
    submit = SubmitField("Salvar")

class NotaForm(FlaskForm):
    client_id = SelectField("Cliente", coerce=int, validators=[DataRequired()])
    modelo = SelectField("Modelo", choices=[("55", "NF-e"), ("65", "NFC-e")], default="55")
    serie = StringField("Série", default="1", validators=[Optional()])
    numero = IntegerField("Número", validators=[Optional()])
    emitente_cnpj = StringField("Emitente CNPJ", validators=[Optional()])
    valor_total = DecimalField("Valor Total", validators=[Optional()])
    status = SelectField("Status", choices=[
        ("rascunho", "Rascunho"),
        ("emitida", "Emitida"),
        ("cancelada", "Cancelada")
    ], default="rascunho")
    submit = SubmitField("Salvar")
    # Campos dinâmicos de itens serão processados no backend via request.form.getlist(...)
