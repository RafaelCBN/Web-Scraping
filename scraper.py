from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import random

#func aux

def limpar_preco(texto_preco):
    """Extrai primeiro número que parece preço, converte para float."""
    if not texto_preco:
        return 0.0
    try:
        s = str(texto_preco)
        s = re.sub(r'[^\d,\.]', '', s)
        if s.count(',') == 1 and s.count('.') >= 1:
            s = s.replace('.', '').replace(',', '.')
        else:
            s = s.replace(',', '.')
        return float(s) if s else 0.0
    except Exception:
        return 0.0


def get_driver(headless=False):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119 Safari/537.36")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(60)
    return driver


def tentar_aceitar_cookies(driver):
    xpaths = [
        "//button[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'continuar')]",
        "//button[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'aceit')]",
        "//button[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'fechar')]",
        "//a[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'aceit')]",
    ]
    for xp in xpaths:
        try:
            btn = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, xp)))
            btn.click()
            return True
        except Exception:
            continue
    try:
        driver.execute_script("""
            document.querySelectorAll('[id*="cookie"],[class*="cookie"],[id*="consent"],[class*="consent"]').forEach(e => e.remove());
        """)
        return True
    except Exception:
        return False


#extraindo o produto

def extrair_produto_individual(driver, url):
    produto_dados = {'sku': "N/A", 'titulo': "N/A", 'preco': 0.0, 'preco_pix': 0.0,
                     'valor_parcela': 0.0, 'num_parcelas': 0, 'info_tecnicas': "N/A"}
    try:
        driver.get(url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(0.8)

        #nome
        try:
            titulo_el = driver.find_element(By.CSS_SELECTOR, "h1.product-title")
            titulo_completo = titulo_el.text.strip()
        except:
            titulo_completo = driver.title or ""
        produto_dados['titulo'] = re.sub(r'\(Cód\..*\)', '', titulo_completo).strip()

        #SKU
        match_sku = re.search(r'\(Cód\.(.*?)\)', titulo_completo)
        if match_sku:
            produto_dados['sku'] = match_sku.group(1).strip()
        else:
            try:
                el = driver.find_element(By.CSS_SELECTOR, "[data-sku]")
                produto_dados['sku'] = el.get_attribute("data-sku") or produto_dados['sku']
            except:
                pass

        #preco
        try:
            el_preco = driver.find_element(By.CSS_SELECTOR, "span.price-sales")
            texto = el_preco.get_attribute('innerText')
            preco_match = re.search(r'R\$[\s\d\.,]+', texto)
            if preco_match:
                produto_dados['preco'] = limpar_preco(preco_match.group())
        except:
            pass

        #pix
        try:
            el_pix = driver.find_element(By.ID, "pixChangePrice")
            produto_dados['preco_pix'] = limpar_preco(el_pix.text)
        except:
            pass

        #parcelas
        try:
            parcelas_num = driver.find_element(By.CSS_SELECTOR, "span.installments-number").text.strip()
            parcelas_val = driver.find_element(By.CSS_SELECTOR, "span.installments-amount").text.strip()
            produto_dados['num_parcelas'] = int(re.search(r'\d+', parcelas_num).group())
            produto_dados['valor_parcela'] = limpar_preco(parcelas_val)
        except:
            pass

        #info técnicas
        try:
            info_el = driver.find_element(By.CSS_SELECTOR, "div.row.product-detail-description")
            produto_dados['info_tecnicas'] = info_el.text.strip().replace('\n', ' | ')
        except:
            pass

        return produto_dados

    except Exception as e:
        print(f"Erro ao extrair {url}: {e}")
        return None


#busca de produtos

def buscar_produtos(termo_busca, headless=False):
    termo_normalizado = termo_busca.strip().lower()
    url_busca = f"https://www.lojamaeto.com/search/?q={termo_normalizado.replace(' ', '+')}"
    print(f"Buscando em: {url_busca}")

    driver = None
    lista_de_produtos = []
    try:
        driver = get_driver(headless=headless)
        driver.get(url_busca)
        tentar_aceitar_cookies(driver)
        time.sleep(1.0)

        elementos = driver.find_elements(By.CSS_SELECTOR, "a.vtex-product-summary-2-x-clearLink, a")
        candidatos = []
        seen = set()
        for el in elementos:
            try:
                href = el.get_attribute('href')
                if not href or href in seen:
                    continue
                seen.add(href)
                title = (el.get_attribute('aria-label') or el.get_attribute('title') or el.text or "").strip()
                candidatos.append({'title': title, 'href': href})
            except Exception:
                continue

        produtos_filtrados = [c for c in candidatos if termo_normalizado in c['title'].lower()]

        print("Produtos filtrados:")
        for p in produtos_filtrados:
            print(f" - {p['title']}")

        for cand in produtos_filtrados:
            time.sleep(random.uniform(0.8, 2.0))
            produto = extrair_produto_individual(driver, cand['href'])
            if produto:
                lista_de_produtos.append(produto)

    except Exception as e:
        print(f"Erro geral na busca: {e}")
    finally:
        if driver:
            driver.quit()
    return lista_de_produtos
