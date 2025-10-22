from pynfe.entidades.emitente import Emitente
from pynfe.entidades.cliente import Cliente
from pynfe.entidades.notafiscal import NotaFiscal
from pynfe.entidades.produto import Produto
from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.processamento.serializacao import SerializacaoXML
from datetime import datetime
import os

# Caminho do certificado digital A1 (.pfx)
CERT_PATH = os.path.abspath("certificado.pfx")
CERT_PASS = "1234"  # senha do certificado

# Cria o objeto de assinatura
assinatura = AssinaturaA1(CERT_PATH, CERT_PASS)

# --- Emitente (empresa que emite a nota) ---
emitente = Emitente(
    razao_social="Supermercado Duda LTDA",
    nome_fantasia="Super Duda",
    cnpj="12345678000199",
    inscricao_estadual="123456789",
    endereco_logradouro="Rua Central",
    endereco_numero="100",
    endereco_bairro="Centro",
    endereco_municipio="Alenquer",
    endereco_uf="PA",
    endereco_cep="68200000",
    telefone="93999999999",
    email="contato@superduda.com.br"
)

# --- Cliente / Destinatário ---
cliente = Cliente(
    razao_social="Maria Souza",
    cnpj_cpf="98765432100",
    endereco_logradouro="Rua das Flores",
    endereco_numero="50",
    endereco_bairro="Centro",
    endereco_municipio="Alenquer",
    endereco_uf="PA",
    endereco_cep="68200000",
    telefone="93988888888",
    email="maria.souza@email.com"
)

# --- Criação da Nota Fiscal ---
nota = NotaFiscal(
    emitente=emitente,
    cliente=cliente,
    natureza_operacao="Venda de Mercadoria",
    tipo_operacao=1,  # 1 = saída, 0 = entrada
    modelo="55",
    serie="1",
    numero_nf="1001",
    data_emissao=datetime.now(),
    data_saida_entrada=datetime.now()
)

# --- Adiciona um produto ---
produto = Produto(
    codigo="001",
    descricao="Arroz Tipo 1 5kg",
    ncm="10063011",
    cfop="5102",
    unidade_comercial="UN",
    quantidade_comercial=1,
    valor_unitario_comercial=25.00,
    valor_total_bruto=25.00
)

# Adiciona produto à nota
nota.adicionar_produto(produto)

# --- Serializa e Assina o XML ---
serializador = SerializacaoXML(versao="4.00", homologacao=True)
xml_gerado = serializador.exportar_nota_fiscal(nota)
xml_assinado = assinatura.assinar(xml_gerado)

# --- Salva o XML gerado ---
os.makedirs("notas_geradas", exist_ok=True)
with open("notas_geradas/nfe_assinada.xml", "wb") as f:
    f.write(xml_assinado)

print("✅ NF-e XML gerado e assinado com sucesso!")
print("📄 Arquivo salvo em: notas_geradas/nfe_assinada.xml")
