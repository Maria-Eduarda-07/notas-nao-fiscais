from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired


class ClientForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    cpf_cnpj = StringField('CPF/CNPJ')
    endereco = StringField('Endereco')
    submit = SubmitField('Salvar')

class ProductForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    preco = DecimalField('Preço', validators=[DataRequired()])
    estoque = IntegerField('Estoque')
    submit = SubmitField('Salvar')
