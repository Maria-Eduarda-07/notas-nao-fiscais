import os
import uuid
from datetime import datetime
from io import BytesIO
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from weasyprint import HTML
from config import Config
from models import db, User, Client, Product, Invoice, InvoiceItem
from forms import LoginForm, ClientForm, ProductForm


# --- Criação da aplicação ---
app = Flask(__name__, static_folder="static", template_folder="templates")
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

# --- Login ---
login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# --- Criação de tabelas no primeiro start ---
with app.app_context():
    db.create_all()

from werkzeug.security import generate_password_hash
from models import User

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username="admin").first():
        admin = User(
            username="admin",
            password_hash=generate_password_hash("admin123")
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin criado automaticamente (admin / admin123)")

# --- ROTAS ---

@app.route("/")
@login_required
def index():
    notas = Invoice.query.order_by(Invoice.data.desc()).all()
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
        c = Client(
            nome=form.nome.data,
            cpf_cnpj=form.cpf_cnpj.data,
            endereco=form.endereco.data,
            email=form.email.data
        )
        db.session.add(c)
        db.session.commit()
        flash("Cliente salvo com sucesso!", "success")
        return redirect(url_for("clientes"))
    clients = Client.query.all()
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


@app.route("/nova_nota", methods=["GET", "POST"])
@login_required
def nova_nota():
    clients = Client.query.all()
    products = Product.query.all()

    if request.method == "POST":
        tipo = request.form.get("tipo") or "nao_fiscal"
        cliente_id = request.form.get("cliente") or None

        itens = []
        total = 0
        idx = 0
        while True:
            desc = request.form.get(f"item-{idx}-desc")
            if not desc:
                break
            qty = int(request.form.get(f"item-{idx}-qty") or 1)
            price = float(request.form.get(f"item-{idx}-price") or 0)
            total += qty * price
            itens.append({"descricao": desc, "quantidade": qty, "preco_unit": price})
            idx += 1

        numero = f"NF-{uuid.uuid4().hex[:8].upper()}"
        inv = Invoice(numero=numero, tipo=tipo, cliente_id=cliente_id, data=datetime.utcnow(), total=total)
        db.session.add(inv)
        db.session.flush()

        for it in itens:
            item = InvoiceItem(
                invoice_id=inv.id,
                descricao=it["descricao"],
                quantidade=it["quantidade"],
                preco_unit=it["preco_unit"]
            )
            db.session.add(item)

        db.session.commit()
        flash("Nota criada com sucesso!", "success")
        return redirect(url_for("index"))

    return render_template("nova_nota.html", clients=clients, products=products)


@app.route("/nota/<int:nota_id>/pdf")
@login_required
def nota_pdf(nota_id):
    inv = Invoice.query.get_or_404(nota_id)
    cliente = inv.cliente
    itens = inv.itens
    total = float(inv.total or sum([float(i.preco_unit) * i.quantidade for i in itens]))
    html = render_template("nota_pdf.html", nota=inv, cliente=cliente, itens=itens, total=total)
    pdf = HTML(string=html, base_url=request.base_url).write_pdf()
    return send_file(BytesIO(pdf), download_name=f"nota-{inv.numero}.pdf", as_attachment=True)


# --- Rota de teste para Render ---
@app.route("/ping")
def ping():
    return "✅ Sistema de Notas App ativo no Render!"


# --- Execução local ---
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
