from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Optional

class LoginForm(FlaskForm):
    username = StringField("Usuário", validators=[DataRequired()])
    password = PasswordField("Senha", validators=[DataRequired()])
    submit = SubmitField("Entrar")

class ClientForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
    cpf_cnpj = StringField("CPF/CNPJ", validators=[Optional()])
    endereco = StringField("Endereço", validators=[Optional()])
    email = StringField("E-mail", validators=[Optional()])
    submit = SubmitField("Salvar")

class ProductForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
    preco_unit = DecimalField("Preço", validators=[DataRequired()])
    estoque = IntegerField("Estoque", validators=[Optional()])
    submit = SubmitField("Salvar")

