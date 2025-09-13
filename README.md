# Web Scraping - Loja Maeto

Este projeto é um scraper em Python que coleta informações de produtos do site [Loja Maeto](https://www.lojamaeto.com).  
Ele permite buscar produtos por **nome**, extrair detalhes como preço, preço PIX, parcelamento e informações técnicas, e salvar no banco de dados SQLite.

---

## Funcionalidades

- Buscar produtos por **nome**.
- Extrair:
  - Título
  - SKU
  - Preço principal
  - Preço PIX
  - Parcelamento
  - Informações técnicas
- Salvar os resultados no banco de dados SQLite (`produtos.db`).
- Listar produtos já salvos.
- Apagar resultados antigos do banco.

---

## Pré-requisitos

- Python 3.11 ou superior
- Google Chrome instalado
- [ChromeDriver](https://sites.google.com/chromium.org/driver/) (gerenciado automaticamente pelo `webdriver-manager`)
- Recomenda-se criar um **ambiente virtual** para instalar dependências do projeto.

---

## Instalação

1. Clone o repositório:

-bash
git clone https://github.com/RafaelCBN/Web-Scraping.git
cd Web-Scraping

Crie e ative um ambiente virtual (opcional, mas recomendado):
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / Mac
python3 -m venv venv
source venv/bin/activate

##Instale as dependências:

pip install -r requirements.txt

Execute o arquivo principal:
python main.py

Você verá um menu com as seguintes opções:

<img width="1248" height="1032" alt="image" src="https://github.com/user-attachments/assets/f2603f1d-5e34-4fbd-bf60-00ce678308ce" />


Buscar produto – Digite o nome ou SKU do produto.
Apagar resultados antigos do banco – Limpa todos os produtos salvos.
Ver produtos salvos – Lista os produtos atualmente no banco.
Sair – Fecha o programa.

Exemplo de busca por nome:
Digite o nome do produto que deseja buscar: luva

####OBS####

O scraper utiliza Selenium com Chrome. Se houver atualização do navegador, o webdriver-manager gerencia automaticamente o ChromeDriver.
O ambiente virtual garante que versões de pacotes não conflitem com outros projetos.
Os produtos são salvos em produtos.db para consulta futura.
