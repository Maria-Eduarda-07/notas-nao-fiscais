from playwright.sync_api import sync_playwright
import pytest

BASE_URL = "https://notas-app-1.onrender.com"
USERNAME = "admin"
PASSWORD = "admin123"

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    page = browser.new_page()
    yield page
    page.close()

def test_login_and_create_invoice(page):
    # Acessa a página de login
    page.goto(f"{BASE_URL}/login")
    
    # Preenche usuário e senha usando IDs
    page.fill('#username', USERNAME)
    page.fill('#password', PASSWORD)
    
    # Clica no botão Entrar usando o id do input
    page.click('#submit')
    
    # Espera redirecionamento
    page.wait_for_load_state("networkidle")
    
    # Verifica que não ficou na página de login
    assert "/login" not in page.url, "Login falhou"
    
    # --- Criar nota de teste ---
    if page.locator('text=Criar Nota').count() > 0:
        page.click('text=Criar Nota')
        page.wait_for_load_state("networkidle")

        # Preencher campos da nota (ajuste conforme sua UI)
        if page.locator('input[placeholder="Cliente"]').count() > 0:
            page.fill('input[placeholder="Cliente"]', 'Cliente Teste')
        if page.locator('input[placeholder="Descrição"]').count() > 0:
            page.fill('input[placeholder="Descrição"]', 'Serviço de teste')
        if page.locator('input[placeholder="Quantidade"]').count() > 0:
            page.fill('input[placeholder="Quantidade"]', '1')
        if page.locator('input[placeholder="Preço"]').count() > 0:
            page.fill('input[placeholder="Preço"]', '100.00')

        # Salvar
        if page.locator('button:has-text("Salvar")').count() > 0:
            page.click('button:has-text("Salvar")')
            page.wait_for_timeout(1000)

        # Checar mensagem de sucesso
        success_text = page.locator('text=sucesso').first
        assert success_text.count() > 0, "Nota não foi criada com sucesso"
