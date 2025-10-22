from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import io


def gerar_pdf(nota):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setFont("Helvetica", 12)

    c.drawString(30 * mm, 270 * mm, f"Nota Não Fiscal Nº {nota.numero}")
    c.line(25 * mm, 268 * mm, 185 * mm, 268 * mm)

    c.drawString(30 * mm, 255 * mm, f"Cliente: {nota.cliente_nome}")
    c.drawString(30 * mm, 245 * mm, f"CPF: {nota.cliente_cpf}")
    c.drawString(30 * mm, 235 * mm, f"Descrição: {nota.descricao}")
    c.drawString(30 * mm, 225 * mm, f"Valor Total: R$ {nota.valor_total:.2f}")
    c.drawString(30 * mm, 215 * mm,
                 f"Data de Emissão: {nota.data_emissao.strftime('%d/%m/%Y %H:%M')}")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.read()
