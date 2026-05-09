import sqlite3
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

caminho_banco = os.path.join(BASE_DIR, "estoque.db")

def conectar_banco():
    conexao = sqlite3.connect(caminho_banco)
    cursor = conexao.cursor()
    return conexao, cursor

def criar_tabela():
    conexao, cursor = conectar_banco()
   
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT,
            quantidade INTEGER NOT NULL,
            estoque_minimo INTEGER,
            preco REAL
        )
    ''')
    conexao.commit()    
    conexao.close()