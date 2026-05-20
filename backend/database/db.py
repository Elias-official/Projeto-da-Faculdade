import sqlite3
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

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
                produto TEXT NOT NULL,
                categoria TEXT NOT NULL,
                estoque_atual INTEGER NOT NULL,
                estoque_minimo INTEGER NOT NULL,
                preco REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'Normal'
            )
        ''')
        conn.commit()
        _migrar_tabela_produtos(conn, cursor)
    # criar outras tabelas relacionadas
    criar_tabela_movimentacoes()
    criar_tabela_categorias()
    criar_tabela_usuarios()


def _migrar_tabela_produtos(conn, cursor):
    cursor.execute("PRAGMA table_info(produtos)")
    cols = [row[1] for row in cursor.fetchall()]

    if not cols:
        return

    if 'produto' not in cols and 'nome' in cols:
        cursor.execute('ALTER TABLE produtos RENAME TO produtos_old')
        cursor.execute('''
            CREATE TABLE produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto TEXT NOT NULL,
                categoria TEXT NOT NULL,
                estoque_atual INTEGER NOT NULL,
                estoque_minimo INTEGER NOT NULL,
                preco REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'Normal'
            )
        ''')
        cursor.execute('''
            INSERT INTO produtos (produto, categoria, estoque_atual, estoque_minimo, preco, status)
            SELECT nome, categoria, quantidade, estoque_minimo, preco, 'Normal'
            FROM produtos_old
        ''')
        cursor.execute('DROP TABLE produtos_old')
        conn.commit()

    elif 'produto' in cols and 'status' not in cols:
        cursor.execute('ALTER TABLE produtos RENAME TO produtos_old')
        cursor.execute('''
            CREATE TABLE produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto TEXT NOT NULL,
                categoria TEXT NOT NULL,
                estoque_atual INTEGER NOT NULL,
                estoque_minimo INTEGER NOT NULL,
                preco REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'Normal'
            )
        ''')
        cursor.execute('''
            INSERT INTO produtos (produto, categoria, estoque_atual, estoque_minimo, preco, status)
            SELECT produto, categoria, estoque_atual, estoque_minimo, preco, 'Normal'
            FROM produtos_old
        ''')
        cursor.execute('DROP TABLE produtos_old')
        conn.commit()

#TABELA MOVIMENTAÇÕES

def criar_tabela_movimentacoes():
    with conectar_banco() as conn:
        cursor = conn.cursor()
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
        conn.commit()

def criar_tabela_categorias():

    with conectar_banco() as conn:

        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias (
                       
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                       
                nome TEXT NOT NULL UNIQUE
            )
        ''')

        categorias_padrao = [
            'Informática',
            'Celulares',
            'Periféricos',
            'Redes',
            'Escritório',
            'Acessórios'
        ]

        cursor.executemany('''
            INSERT OR IGNORE INTO categorias (nome)
             VALUES (?)
        ''', [(categoria,) for categoria in categorias_padrao])

        conn.commit()

def inserir_produtos_padrao():

    with conectar_banco() as conn:

        cursor = conn.cursor()

        produtos = [

            ('Notebook Dell', 'Informática', 15, 5, 3500.00, 'Normal'),

            ('iPhone 13', 'Celulares', 8, 3, 5200.00, 'Normal'),

            ('Mouse Gamer', 'Periféricos', 4, 5, 150.00, 'Atenção'),

            ('Roteador TP-Link', 'Redes', 2, 3, 280.00, 'Crítico'),

            ('Cadeira Escritório', 'Escritório', 10, 2, 900.00, 'Normal'),

            ('Carregador USB-C', 'Acessórios', 20, 5, 80.00, 'Normal')

        ]

        cursor.executemany('''
            INSERT OR IGNORE INTO produtos
            (
                produto,
                categoria,
                estoque_atual,
                estoque_minimo,
                preco,
                status
            )

            VALUES (?, ?, ?, ?, ?, ?)

        ''', produtos)

        conn.commit()

def movimentações_tabela():

    with conectar_banco() as conn:

        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE movimentacoes (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                produto_id INTEGER NOT NULL,

                usuario_id INTEGER NOT NULL,

                tipo TEXT NOT NULL,

                quantidade INTEGER NOT NULL,

                data_movimentacao TEXT NOT NULL,

                FOREIGN KEY (produto_id)
                REFERENCES produtos(id),

                FOREIGN KEY (usuario_id)
                REFERENCES usuarios(id)
            )
         )
        ''')

        conn.commit()
def usuarios_tabela():

    with conectar_banco() as conn:

        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE usuarios (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                nome TEXT NOT NULL,

                usuario TEXT NOT NULL UNIQUE,

                senha TEXT NOT NULL,

                cargo TEXT NOT NULL
            )
        ''')

        conn.commit()


def criar_tabela_usuarios():
    with conectar_banco() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL
            )
        ''')
        conn.commit()


def inserir_usuarios_padrao():
    with conectar_banco() as conn:
        cursor = conn.cursor()
        # cria usuário admin padrão se não existir
        senha_hash = generate_password_hash('admin123')
        try:
            cursor.execute('INSERT OR IGNORE INTO usuarios (username, senha) VALUES (?, ?)', ('admin', senha_hash))
            conn.commit()
        except Exception:
            conn.rollback()