from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from models import db, Client, Product, Invoice, InvoiceItem
from datetime import datetime
from io import BytesIO
from weasyprint import HTML

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notas.db'
app.config['SECRET_KEY'] = 'chave-secreta'

db.init_app(app)

# Cria o banco de dados ao iniciar o app (compatível com Flask 3.1+)
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    notas = Invoice.query.order_by(Invoice.data.desc()).all()
    return render_template('index.html', notas=notas)


@app.route('/nova_nota', methods=['GET', 'POST'])
def nova_nota():
    if request.method == 'POST':
        cliente_nome = request.form['cliente']
        tipo_nota = request.form['tipo']
        descricao = request.form['descricao']
        valor = float(request.form['valor'])

        cliente = Client.query.filter_by(nome=cliente_nome).first()
        if not cliente:
            cliente = Client(nome=cliente_nome)
            db.session.add(cliente)
            db.session.commit()

        nota = Invoice(cliente_id=cliente.id, tipo=tipo_nota, data=datetime.utcnow())
        db.session.add(nota)
        db.session.commit()

        item = InvoiceItem(invoice_id=nota.id, descricao=descricao, preco_unit=valor)
        db.session.add(item)
        db.session.commit()

        flash('Nota criada com sucesso!')
        return redirect(url_for('index'))

    return render_template('nova_nota.html')


@app.route('/nota/<int:nota_id>')
def gerar_pdf(nota_id):
    nota = Invoice.query.get_or_404(nota_id)
    cliente = Client.query.get(nota.cliente_id)
    itens = InvoiceItem.query.filter_by(invoice_id=nota.id).all()
    total = sum([i.preco_unit for i in itens])

    html = render_template('notas.html', nota=nota, cliente=cliente, itens=itens, total=total)
    pdf = HTML(string=html).write_pdf()

    return send_file(BytesIO(pdf), as_attachment=True, download_name=f"nota_{nota.id}.pdf")


# 🔥 Rodar localmente ou em produção (Render / Railway)
if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080)
