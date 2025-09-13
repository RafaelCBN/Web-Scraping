from scraper import buscar_produtos
import sqlite3
import json

DB_NAME = "produtos.db"

def criar_tabela():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            sku TEXT PRIMARY KEY,
            titulo TEXT,
            preco REAL,
            preco_pix REAL,
            valor_parcela REAL,
            num_parcelas INTEGER,
            info_tecnicas TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_product(produto):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO produtos
        (sku, titulo, preco, preco_pix, valor_parcela, num_parcelas, info_tecnicas)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        produto['sku'],
        produto['titulo'],
        produto['preco'],
        produto['preco_pix'],
        produto['valor_parcela'],
        produto['num_parcelas'],
        produto['info_tecnicas']
    ))
    conn.commit()
    conn.close()

def ver_produtos():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    if not produtos:
        print("\nO banco de dados está vazio.")
    else:
        for i, p in enumerate(produtos, 1):
            print(f"\n[Produto {i}]")
            print(f"SKU           : {p[0]}")
            print(f"Título        : {p[1]}")
            print(f"Preço         : R$ {p[2]:.2f}")
            print(f"Preço PIX     : R$ {p[3]:.2f}")
            print(f"Parcelamento  : {p[5]}x de R$ {p[4]:.2f}")
            print(f"Info Técnicas : {p[6]}")
    conn.close()

def apagar_produtos():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos")
    conn.commit()
    conn.close()
    print("Todos os resultados foram apagados com sucesso!")

def menu_buscar_produto():
    termo = input("Digite o nome ou SKU do produto que deseja buscar: ")
    resultados = buscar_produtos(termo, headless=False)
    if resultados:
        for r in resultados:
            insert_product(r)
        print(f"{len(resultados)} produtos salvos/atualizados no banco.")
    else:
        print("Nenhum produto foi extraído.")

def main():
    criar_tabela()
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Buscar produto")
        print("2. Apagar resultados antigos do banco")
        print("3. Ver produtos salvos")
        print("4. Sair")
        opc = input("Escolha uma opção: ")
        if opc == "1":
            menu_buscar_produto()
        elif opc == "2":
            confirmar = input("Tem certeza que deseja apagar todos os resultados antigos? (s/n): ")
            if confirmar.lower() == "s":
                apagar_produtos()
        elif opc == "3":
            ver_produtos()
        elif opc == "4":
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
