from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class NotaNaoFiscalForm(FlaskForm):
    cliente_nome = StringField("Nome do Cliente", validators=[
                               DataRequired(), Length(max=100)])
    cliente_cpf = StringField("CPF", validators=[Length(max=14)])
    descricao = TextAreaField("Descrição", validators=[
                              DataRequired(), Length(max=255)])
    valor_total = DecimalField("Valor Total (R$)", validators=[DataRequired()])
    submit = SubmitField("Emitir Nota")
