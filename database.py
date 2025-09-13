# database.py

import sqlite3

DB_NAME = "produtos.db"

def inicializar_banco():
    """Garante que o banco de dados e a tabela existam."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            sku TEXT PRIMARY KEY,
            titulo TEXT NOT NULL,
            preco REAL,
            preco_pix REAL,
            valor_parcela REAL,
            num_parcelas INTEGER,
            info_tecnicas TEXT
        )
    ''')
    conn.commit()
    conn.close()

def salvar_produtos_em_lote(produtos):
    """Salva uma lista de produtos no banco, substituindo se o SKU já existir."""
    if not produtos:
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    dados_para_inserir = [
        (
            p.get("sku", "N/A"),
            p.get("titulo", "N/A"),
            p.get("preco", 0.0),
            p.get("preco_pix", 0.0),
            p.get("valor_parcela", 0.0),
            p.get("num_parcelas", 0),
            p.get("info_tecnicas", "N/A")
        )
        for p in produtos
    ]

    cursor.executemany('''
        INSERT OR REPLACE INTO produtos (
            sku, titulo, preco, preco_pix, valor_parcela, num_parcelas, info_tecnicas
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', dados_para_inserir)

    conn.commit()
    conn.close()
    print(f"{len(produtos)} produtos salvos/atualizados no banco.")