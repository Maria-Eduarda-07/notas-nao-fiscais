# teste/test_suite_online.py
import os
import time
import requests
from pathlib import Path
from datetime import datetime
import pytest
from playwright.sync_api import sync_playwright, expect
from PyPDF2 import PdfReader

# --------------------------
# CONFIGURAÇÃO
# --------------------------
BASE_URL = os.getenv("NOTAS_BASE_URL", "https://notas-app-1.onrender.com")
ADMIN_USER = os.getenv("NOTAS_USER", "admin")
ADMIN_PASS = os.getenv("NOTAS_PASS", "admin123")
HEADLESS = os.getenv("HEADLESS", "1") == "1"

ROOT = Path(__file__).parent
DOWNLOADS = ROOT / "downloads"
ARTIFACTS = ROOT / "artifacts"
DOWNLOADS.mkdir(exist_ok=True)
ARTIFACTS.mkdir(exist_ok=True)

# ---------- HELPERS ----------
def ts():
    return datetime.now().strftime("%Y%m%d-%H%M%S")

def wait_app_ready(timeout=120):
    """Tenta acessar o site até receber código 200 ou timeout."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(BASE_URL, timeout=10)
            if r.status_code == 200:
                print("✅ Aplicação está pronta!")
                return True
        except Exception:
            pass
        print("⏳ Aguardando app acordar...")
        time.sleep(5)
    raise TimeoutError("O app não respondeu em tempo hábil.")

def save_failure_artifacts(page, name_prefix):
    """Salvar screenshot e HTML do estado atual para debug quando houver falha."""
    t = ts()
    screenshot_path = ARTIFACTS / f"{name_prefix}_{t}.png"
    html_path = ARTIFACTS / f"{name_prefix}_{t}.html"
    try:
        page.screenshot(path=str(screenshot_path), full_page=True)
    except Exception as e:
        print("Erro ao tirar screenshot:", e)
    try:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(page.content())
    except Exception as e:
        print("Erro ao salvar HTML:", e)
    return screenshot_path, html_path

def validate_pdf_contains(path: Path, expected_texts: list[str]):
    reader = PdfReader(str(path))
    text = ""
    for p in reader.pages:
        extracted = p.extract_text() or ""
        text += extracted
    for expected in expected_texts:
        assert expected in text, f"'{expected}' não encontrado no PDF ({path.name})"

# --------------------------
# FIXTURES
# --------------------------
@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(headless=HEADLESS)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def context(browser, request):
    # criar contexto que aceita downloads e com viewport padrão
    context = browser.new_context(accept_downloads=True)
    page = context.new_page()
    yield page
    # on teardown, se falhou, o hook abaixo salva artefatos via pytest hook
    page.close()
    context.close()

# Hook do pytest para salvar screenshot/HTML quando o teste falhar
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # executa as outras implementações primeiro
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        # tenta recuperar fixture 'context' (page) do item
        page = item.funcargs.get("context") or item.funcargs.get("page")
        if page:
            name = item.name.replace("/", "_")
            save_failure_artifacts(page, f"FAIL-{name}")

# --------------------------
# AÇÕES COMUNS (utilitárias)
# --------------------------
def do_login(page, user=ADMIN_USER, pwd=ADMIN_PASS):
    page.goto(BASE_URL)
    page.wait_for_selector("#username")
    page.fill("#username", user)
    page.fill("#password", pwd)
    # clicar no input submit que existe no site
    page.click('input[value="Entrar"]')
    # esperar a navegação estabilizar
    page.wait_for_load_state("networkidle")

def ensure_logged_in(page):
    # se já estiver logado, retornar True; senão tenta logar
    page.goto(BASE_URL)
    if page.locator('text="+ Nova Nota"').count() > 0:
        return True
    do_login(page)
    return True

def create_client_if_needed(page, name="Cliente Automático", email="cliente.auto@example.com"):
    # tenta ir pra página de clientes e criar
    ensure_logged_in(page)
    # abrir tela de novo cliente (se tiver link)
    if page.locator('text="+ Novo Cliente"').count() > 0:
        page.click('text="+ Novo Cliente"')
        page.wait_for_selector('#name')
        page.fill('#name', name)
        page.fill('#email', email)
        # tentar clicar submit (botão ou input)
        if page.locator('button[type="submit"]').count() > 0:
            page.click('button[type="submit"]')
        else:
            page.click('input[type="submit"]')
        page.wait_for_load_state("networkidle")
        return True
    # fallback: talvez o app não tenha UI para criar cliente — ignore
    return False

def create_invoice_via_ui(page, client_index=1, description="Serviço Automático", qty=1, price=123.45):
    ensure_logged_in(page)

    # tenta acessar a página de nova nota
    page.goto(f"{BASE_URL}/nova_nota")
    page.wait_for_load_state("networkidle")
    time.sleep(1.5)

    # 🧩 CLIENTE
    selectors_client = ["#client_id", "#cliente", "select[name='cliente']", "input[name='cliente']"]
    client_selected = False

    for sel in selectors_client:
        if page.locator(sel).count() > 0:
            el = page.locator(sel).first
            tag_name = el.evaluate("el => el.tagName.toLowerCase()")
            if tag_name == "select":
                try:
                    # tenta selecionar pelo índice, se possível
                    options = el.locator("option").all()
                    if len(options) > 1:
                        page.select_option(sel, index=client_index)
                    else:
                        page.select_option(sel, index=0)
                    client_selected = True
                    break
                except Exception as e:
                    print(f"⚠️ Falha ao selecionar cliente: {e}")
            else:
                page.fill(sel, f"Cliente {ts()}")
                client_selected = True
                break

    if not client_selected:
        raise AssertionError("Nenhum campo ou seletor de cliente foi encontrado na página.")

    # 🧾 DESCRIÇÃO
    selectors_desc = ["#description", "#descricao", "input[name='descricao']", "textarea[name='descricao']"]
    for sel in selectors_desc:
        if page.locator(sel).count() > 0:
            page.fill(sel, description)
            break

    # 🔢 QUANTIDADE
    selectors_qty = ["#quantity", "#quantidade", "input[name='quantidade']"]
    for sel in selectors_qty:
        if page.locator(sel).count() > 0:
            page.fill(sel, str(qty))
            break

    # 💰 PREÇO
    selectors_price = ["#price", "#valor", "input[name='valor']", "input[name='preco']"]
    for sel in selectors_price:
        if page.locator(sel).count() > 0:
            page.fill(sel, str(price))
            break

    # 💾 SALVAR/GERAR NOTA
    selectors_submit = [
        'button[type="submit"]',
        'input[type="submit"]',
        'text=Salvar',
        'text=Emitir',
        'text=Gerar Nota',
        'text=Criar Nota',
    ]
    clicked = False
    for sel in selectors_submit:
        if page.locator(sel).count() > 0:
            page.click(sel)
            clicked = True
            break

    if not clicked:
        raise AssertionError("Nenhum botão de salvar/enviar nota encontrado na página.")

    # aguardar carregamento da resposta
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    # verificar se há mensagem de sucesso
    success_indicators = ["sucesso", "nota criada", "nota emitida", "nota gerada"]
    content = page.content().lower()
    if not any(msg in content for msg in success_indicators):
        # salvar screenshot e falhar
        save_failure_artifacts(page, "create_invoice_failed")
        raise AssertionError("Nenhuma confirmação de criação de nota encontrada na página.")

# --------------------------
# TESTS
# --------------------------
def test_homepage_loads(context):
    wait_app_ready()  # 🔥 garante que o Render está ativo
    page = context
    page.goto(BASE_URL, wait_until="networkidle", timeout=60000)
    title = page.title()
    assert "Notas" in title or "Login" in title

def test_login_valid(context):
    wait_app_ready()
    page = context
    do_login(page, ADMIN_USER, ADMIN_PASS)

def test_login_invalid(context):
    wait_app_ready()
    page = context
    page.goto(BASE_URL)
    page.wait_for_selector("#username")
    page.fill("#username", "user_incorreto_xyz")
    page.fill("#password", "senha_errada_xyz")
    page.click('input[value="Entrar"]')
    # a aplicação mostra mensagem de erro; aguardamos e verificamos
    page.wait_for_timeout(1000)
    body = page.content().lower()
    assert ("inválido" in body) or ("erro" in body) or ("credenciais" in body)

def test_create_client(context):
    page = context
    do_login(page)
    created = create_client_if_needed(page)
    # se não há UI para criar cliente, aceita-se que a ação foi ignorada
    assert created or page.locator('text="+ Nova Nota"').count() > 0

def test_create_invoice_and_download_pdf(context):
    page = context
    do_login(page)
    # cria cliente se necessário
    create_client_if_needed(page)
    # cria nota
    create_invoice_via_ui(page, client_index=1, description="Serviço Automático", qty=1, price=123.45)
    # visualizar/baixar nota (procura por links com texto Visualizar/Baixar)
    # primeiro tenta encontrar botão/link "Visualizar Nota" ou similar
    if page.locator('text=Visualizar Nota').count() > 0:
        page.click('text=Visualizar Nota')
        page.wait_for_load_state("networkidle")
    # exportar/baixar PDF
    if page.locator('text=Baixar PDF').count() > 0:
        with page.expect_download() as dl:
            page.click('text=Baixar PDF')
        download = dl.value
        filename = f"{DOWNLOADS}/{download.suggested_filename.split('.')[0]}_{ts()}.pdf"
        download.save_as(filename)
        p = Path(filename)
        assert p.exists()
        # validar conteúdo básico do PDF (procura por descrição e preço)
        try:
            validate_pdf_contains(p, ["Serviço Automático", "123"])
        except Exception:
            # se não conseguir validar o PDF, falhar e deixar artefato
            raise

def test_logout(context):
    page = context
    do_login(page)
    # tentar clicar em "Sair" / "logout"
    if page.locator('text="Sair"').count() > 0:
        page.click('text="Sair"')
    elif page.locator('text=Sair').count() > 0:
        page.click('text=Sair')
    else:
        # caso não exista link, test passa se não encontrar +Nova Nota (indicando logout)
        page.goto(BASE_URL + "/logout")
    page.wait_for_timeout(800)
    # verificar se voltou para tela de login
    body = page.content().lower()
    assert ("entrar" in body) or ("login" in body)

# --------------------------
# EXECUTAR MANUAL (opcional)
# --------------------------
if __name__ == "__main__":
    print("Execute via pytest: pytest teste/test_suite_online.py -v --html=relatorio.html --self-contained-html")
