import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_NAME = os.getenv("DB_NAME", "estoque.db")

caminho_banco = os.path.join(BASE_DIR, DB_NAME)

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

    # TABELA MOVIMENTACOES
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            data_movimentacao TEXT NOT NULL,
            FOREIGN KEY (produto_id) REFERENCES produtos(id)
        )
    ''')
    conexao.commit()    
    conexao.close()

   