import sqlite3
import textwrap

DB_NAME = "produtos.db"

def view_data():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT sku, titulo, preco, preco_pix, num_parcelas, valor_parcela, info_tecnicas
            FROM produtos
            ORDER BY titulo
        """)
        products = cursor.fetchall()
        conn.close()

        if not products:
            print(f"\nO banco de dados '{DB_NAME}' está vazio. Rode o 'main.py' para buscar produtos.")
            return

        print(f"\n--- Produtos Salvos em '{DB_NAME}' ---\n")
        for i, p in enumerate(products, 1):
            sku, titulo, preco, preco_pix, num_p, val_p, info = p

            #conversao
            try:
                preco_float = float(preco)
            except (ValueError, TypeError):
                preco_float = 0.0
            try:
                preco_pix_float = float(preco_pix)
            except (ValueError, TypeError):
                preco_pix_float = 0.0
            try:
                val_p_float = float(val_p)
            except (ValueError, TypeError):
                val_p_float = 0.0
            try:
                num_p_int = int(num_p)
            except (ValueError, TypeError):
                num_p_int = 0

            #destaque val
            preco_str = f"R$ {preco_float:.2f}" if preco_float > 0 else "N/A"
            preco_pix_str = f"R$ {preco_pix_float:.2f}" if preco_pix_float > 0 else "N/A"
            parcela_str = f"{num_p_int}x de R$ {val_p_float:.2f}" if num_p_int > 0 else "N/A"

            print(f"[Produto {i}]")
            print(f"  SKU           : {sku}")
            print(f"  Título        : {titulo}")
            print(f"  Preço         : {preco_str}")
            print(f"  Preço PIX     : {preco_pix_str}")
            print(f"  Parcelamento  : {parcela_str}")
            print(f"  Info Técnicas : {textwrap.fill(info or 'N/A', width=80)}")
            print("-" * 80)

    except sqlite3.OperationalError:
        print(f"Erro: O banco de dados '{DB_NAME}' ou a tabela 'produtos' não foram encontrados.")
        print("Certifique-se de executar 'python create_database.py' primeiro.")

if __name__ == "__main__":
    view_data()
