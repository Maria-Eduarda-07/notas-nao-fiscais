from flask_login import AnonymousUserMixin
from flask import Flask, render_template, redirect, url_for, flash, send_file
from models import db, NotaNaoFiscal
from forms import NotaNaoFiscalForm
from utils.gerar_pdf import gerar_pdf
import io
import logging

# ===============================
# ⚙️ Configuração básica do Flask
# ===============================
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notas.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "segredo"

# ===============================


@app.context_processor
def inject_current_user():
    # Garante que 'current_user' sempre existe, mesmo sem Flask-Login
    class DummyUser(AnonymousUserMixin):
        def is_authenticated(self) -> bool:
            return False
            name = "Visitante"
    return {'current_user': DummyUser()}


# Inicializa banco de dados
db.init_app(app)
with app.app_context():
    db.create_all()

# ===============================
# 🧠 Configuração de logs
# ===============================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# ===============================
# 🏠 Rota principal: lista notas
# ===============================


@app.route("/")
def index():
    """Exibe todas as notas não fiscais emitidas"""
    try:
        notas = NotaNaoFiscal.query.order_by(
            NotaNaoFiscal.data_emissao.desc()).all()
        return render_template("lista_notas.html", notas=notas)
    except Exception as e:
        logging.exception("Erro ao carregar lista de notas")
        flash("Erro ao carregar as notas. Verifique os logs.", "danger")
        return render_template("lista_notas.html", notas=[])

# ===============================
# 🧾 Rota: criar nova nota
# ===============================


@app.route("/nova_nota", methods=["GET", "POST"])
def nova_nota():
    """Cria uma nova nota não fiscal"""
    form = NotaNaoFiscalForm()

    if form.validate_on_submit():
        try:
            # Gera o número da nota
            ultimo = NotaNaoFiscal.query.order_by(
                NotaNaoFiscal.numero.desc()).first()
            numero = (ultimo.numero + 1) if ultimo else 1

            # Cria objeto da nota
            nota = NotaNaoFiscal(
                numero=numero,
                cliente_nome=form.cliente_nome.data,
                cliente_cpf=form.cliente_cpf.data,
                descricao=form.descricao.data,
                valor_total=form.valor_total.data,
            )

            # Salva no banco
            db.session.add(nota)
            db.session.commit()

            logging.info(f"Nota não fiscal Nº {numero} emitida com sucesso!")
            flash(
                f"Nota não fiscal Nº {numero} emitida com sucesso!", "success")

            return redirect(url_for("index"))

        except Exception as e:
            logging.exception("Erro ao salvar nova nota")
            flash("Erro ao emitir nota. Verifique os logs.", "danger")
            db.session.rollback()

    return render_template("nova_nota.html", form=form)

# ===============================
# 📄 Rota: gerar PDF da nota
# ===============================


@app.route("/nota/<int:nota_id>/pdf")
def nota_pdf(nota_id):
    """Gera e faz download do PDF da nota"""
    try:
        nota = NotaNaoFiscal.query.get_or_404(nota_id)
        pdf_bytes = gerar_pdf(nota)
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"nota_{nota.numero}.pdf"
        )
    except Exception as e:
        logging.exception("Erro ao gerar PDF da nota")
        flash("Erro ao gerar PDF. Verifique os logs.", "danger")
        return redirect(url_for("index"))


# ===============================
# 🚀 Inicialização do servidor
# ===============================
if __name__ == "__main__":
    logging.info("Servidor Flask iniciado em modo debug.")
    app.run(debug=True)
