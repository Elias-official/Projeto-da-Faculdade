import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.getenv("DB_NAME", "estoque.db")
DB_PATH = os.path.join(BASE_DIR, DB_NAME)


def conectar_banco():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def criar_tabela():
    with conectar_banco() as conn:
        cursor = conn.cursor()
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
        conn.commit()
   