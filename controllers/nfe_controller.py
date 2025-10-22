from pynfe.processamento import ProcessadorNFe
from pynfe.entidades import NotaFiscal, Emitente, Destinatario, Produto
from pynfe.utils.flags import CODIGO_BRASIL
from decimal import Decimal

# --- Configuração do emitente ---
emitente = Emitente(
    razao_social='Minha Empresa LTDA',
    nome_fantasia='SuperMercado Teste',
    cnpj='12345678000199',
    ie='123456789',
    endereco='Rua Exemplo, 123',
    numero='123',
    bairro='Centro',
    municipio='Alenquer',
    uf='PA',
    cep='68200000',
    codigo_municipio=1500404,
    telefone='93999999999'
)

# --- Configuração do destinatário ---
destinatario = Destinatario(
    razao_social='Cliente Teste',
    tipo_documento='CPF',
    numero_documento='12345678909',
    endereco='Rua do Cliente, 456',
    numero='456',
    bairro='Bairro Legal',
    municipio='Alenquer',
    uf='PA',
    cep='68200000',
    codigo_municipio='1500404',
    telefone='93988888888'
)

# --- Produto ---
produto = Produto(
    codigo='001',
    descricao='Produto de Teste',
    ncm='12345678',
    cfop='5102',
    unidade_comercial='UN',
    quantidade_comercial=Decimal('1'),
    valor_unitario_comercial=Decimal('100.00'),
    valor_total_bruto=Decimal('100.00')
)

# --- Nota Fiscal ---
nota = NotaFiscal(
    emitente=emitente,
    destinatario=destinatario,
    uf='PA',
    natureza_operacao='Venda de mercadoria'
)

nota.adicionar_produto(produto)

# --- Processador ---
proc = ProcessadorNFe(uf='PA', ambiente=2)  # 2 = Homologação
xml = proc.gerar_nfe(nota)

# Salva o XML
with open('nota_teste.xml', 'wb') as f:
    f.write(xml)
print("Nota Fiscal Eletrônica gerada com sucesso e salva em 'nota_teste.xml'")