import os
import uuid
from datetime import datetime
from io import BytesIO
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from weasyprint import HTML
from werkzeug.security import generate_password_hash

from config import Config
from models import db, Cliente, Product, Nota, NotaItem, User
from forms import LoginForm, ClientForm, ProductForm, NotaForm

# --- Criação da aplicação ---
app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)
migrate = Migrate(app, db)

# --- Login ---
login_manager = LoginManager(app)
login_manager.login_view = "login" # type: ignore

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# --- Criação de tabelas e usuário admin no primeiro start ---
with app.app_context():
    db.create_all()
    admin_user = User.query.filter_by(username="admin").first()
    if not admin_user:
        admin_user = User(username="admin", password_hash=generate_password_hash("admin123")) # type: ignore
        db.session.add(admin_user)
        db.session.commit()
        print("✅ Usuário admin criado automaticamente (admin / admin123)")
    else:
        print("ℹ️ Usuário admin já existe.")


# --- ROTAS ---
@app.route("/")
@login_required
def index():
    notas = Nota.query.order_by(Nota.data_emissao.desc()).all()
    return render_template("index.html", notas=notas)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("index"))
        flash("Usuário ou senha inválidos", "danger")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/clientes", methods=["GET", "POST"])
@login_required
def clientes():
    form = ClientForm()
    if form.validate_on_submit():
        c = Cliente(
            nome=form.nome.data,
            cpf_cnpj=form.cpf_cnpj.data,
            endereco=form.endereco.data,
            email=form.email.data
        )
        db.session.add(c)
        db.session.commit()
        flash("Cliente salvo com sucesso!", "success")
        return redirect(url_for("clientes"))
    clients = Cliente.query.all()
    return render_template("clientes.html", form=form, clients=clients)


@app.route("/produtos", methods=["GET", "POST"])
@login_required
def produtos():
    form = ProductForm()
    if form.validate_on_submit():
        p = Product(
            nome=form.nome.data,
            preco_unit=form.preco_unit.data,
            estoque=form.estoque.data or 0
        )
        db.session.add(p)
        db.session.commit()
        flash("Produto salvo com sucesso!", "success")
        return redirect(url_for("produtos"))
    produtos = Product.query.all()
    return render_template("produtos.html", form=form, produtos=produtos)


# --- NOVA ROTA /nova_nota (com NCM, CFOP, ICMS etc.) ---
@app.route("/nova_nota", methods=["GET", "POST"])
@login_required
def nova_nota():
    form = NotaForm()
    clientes = Cliente.query.all()

    if request.method == 'POST':
        nota = Nota(
            emitente_cnpj=request.form.get('emitente_cnpj'),
            destinatario_id=request.form.get('client_id') or None,
            valor_total=0
        )
        db.session.add(nota)
        db.session.flush()  # para gerar nota.id

        descricoes = request.form.getlist('item_descricao[]')
        ncm = request.form.getlist('item_ncm[]')
        cfop = request.form.getlist('item_cfop[]')
        qts = request.form.getlist('item_qt[]')
        unids = request.form.getlist('item_un[]')
        prices = request.form.getlist('item_price[]')
        icms = request.form.getlist('item_icms[]')

        total = 0
        for i, desc in enumerate(descricoes):
            q = float(qts[i])
            p = float(prices[i])
            subtotal = q * p
            item = NotaItem(
                nota_id=nota.id,
                descricao=desc,
                ncm=ncm[i] if i < len(ncm) else '',
                cfop=cfop[i] if i < len(cfop) else '',
                quantidade=q,
                unidade=unids[i] if i < len(unids) else '',
                valor_unitario=p,
                icms_aliquota=float(icms[i]) if i < len(icms) and icms[i] else 0
            )
            db.session.add(item)
            total += subtotal

        nota.valor_total = total
        nota.status = 'emitida'
        db.session.commit()
        flash('Nota criada com sucesso', 'success')
        return redirect(url_for('index'))

    return render_template('nova_nota.html', form=form, clientes=clientes)


@app.route("/nota/<int:nota_id>/pdf")
@login_required
def nota_pdf(nota_id):
    nota = Nota.query.get_or_404(nota_id)
    cliente = nota.cliente
    itens = nota.itens
    total = float(nota.valor_total or sum([float(i.valor_unitario) * i.quantidade for i in itens]))
    html = render_template("nota_pdf.html", nota=nota, cliente=cliente, itens=itens, total=total)
    pdf = HTML(string=html, base_url=request.base_url).write_pdf()
    return send_file(BytesIO(pdf), download_name=f"nota-{nota.id}.pdf", as_attachment=True) # type: ignore


@app.route("/ping")
def ping():
    return "✅ Sistema de Notas App ativo no Render!"


# --- Execução local ---
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
