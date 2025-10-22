import os
from decimal import Decimal
from pynfe.processamento.serializacao import SerializacaoXML, SerializacaoQrcode
from pynfe.entidades.emitente import Emitente
from pynfe.entidades.cliente import Cliente
from pynfe.entidades.produto import Produto
from pynfe.entidades.notafiscal import NotaFiscal
from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.processamento.comunicacao import ComunicacaoSefaz
from pynfe.utils import gerar_chave_acesso

# --- Caminho do certificado A1 (.pfx) ---
CERT_PATH = os.path.abspath("certificado.pfx")
CERT_PASS = "senha_certificado"  # altere para sua senha real

# --- Dados da empresa emitente ---
def criar_emitente():
    return Emitente(
        razao_social="Supermercado Duda LTDA",
        nome_fantasia="Supermercado Duda",
        cnpj="12345678000199",
        codigo_de_regime_tributario="1",  # Simples Nacional
        inscricao_estadual="123456789",
        endereco_logradouro="Rua das Flores",
        endereco_numero="123",
        endereco_bairro="Centro",
        endereco_municipio="Alenquer",
        endereco_uf="PA",
        endereco_cep="68200000",
        endereco_pais="Brasil",
        endereco_codigo_municipio="1500404",
    )


def gerar_nfe(dados_cliente, dados_produto):
    emitente = criar_emitente()

    cliente = Cliente(
        razao_social=dados_cliente["nome"],
        tipo_documento="CPF",
        numero_documento=dados_cliente["cpf"],
        endereco_logradouro=dados_cliente["endereco"],
        endereco_numero=dados_cliente["numero"],
        endereco_bairro=dados_cliente["bairro"],
        endereco_municipio=dados_cliente["cidade"],
        endereco_uf=dados_cliente["uf"],
        endereco_cep=dados_cliente["cep"],
        endereco_pais="Brasil",
        endereco_codigo_municipio=dados_cliente["codigo_municipio"],
    )

    produto = Produto(
        codigo="001",
        descricao=dados_produto["descricao"],
        ncm="12345678",
        cfop="5102",
        unidade_comercial="UN",
        quantidade_comercial=Decimal(dados_produto["quantidade"]),
        valor_unitario_comercial=Decimal(dados_produto["valor_unitario"]),
        valor_total_bruto=Decimal(dados_produto["valor_total"]),
        icms_situacao_tributaria="102",
        icms_origem=0,
    )

    nota = NotaFiscal(
        emitente=emitente,
        cliente=cliente,
        ambiente=2,  # 2 = Homologação
        natureza_operacao="Venda de mercadoria",
        tipo_operacao=1  # 1 = Saída
    )

    nota.adicionar_produto(produto)

    # --- Gera chave ---
    nota.chave_acesso = gerar_chave_acesso(
        uf="15", ano=25, mes=10, cnpj=emitente.cnpj,
        modelo="55", serie="1", numero_nf=1, tipo_emissao=1, codigo_nf=12345678
    )

    return nota


def assinar_e_enviar_nfe(nota):
    fonte_dados = FonteDados(nota)  # Cria a fonte de dados a partir da nota
    serializador = SerializacaoXML()
    xml_nfe = serializador.exportar_xml(fonte_dados)  # Passa a fonte_dados como argumento
    return xml_nfe

    # --- Assinar XML ---
    assinatura = AssinaturaA1(CERT_PATH, CERT_PASS)
    xml_assinado = assinatura.assinar(xml_nfe)

    # --- Enviar à SEFAZ ---
    comunicacao = ComunicacaoSefaz(
    uf="PA",
    certificado_arquivo=CERT_PATH,
    certificado_senha=CERT_PASS,
    homologacao=True
    )

    resposta = comunicacao.enviar_nfe(xml_assinado)
    return xml_assinado, resposta
