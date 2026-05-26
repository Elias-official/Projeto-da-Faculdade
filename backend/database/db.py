import os
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.getenv('DB_NAME', 'estoque.db')
DB_PATH = os.path.join(BASE_DIR, DB_NAME)


def conectar_banco():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def criar_tabelas():
    with conectar_banco() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT NOT NULL UNIQUE,
                produto TEXT NOT NULL,
                categoria TEXT NOT NULL,
                marca TEXT NOT NULL,
                estoque_atual INTEGER NOT NULL,
                estoque_minimo INTEGER NOT NULL,
                preco REAL NOT NULL,
                status TEXT NOT NULL,
                criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                cargo TEXT NOT NULL,
                senha TEXT NOT NULL,
                foto_perfil TEXT,
                criado_em TEXT NOT NULL,
                ultimo_login TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movimentacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER NOT NULL,
                usuario_id INTEGER NOT NULL,
                tipo TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                data_movimentacao TEXT NOT NULL,
                FOREIGN KEY(produto_id) REFERENCES produtos(id),
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
            )
        ''')

        conn.commit()
        migrar_schema(conn)


def migrar_schema(conn):
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(produtos)")
    campos_produtos = [row['name'] for row in cursor.fetchall()]

    if 'codigo' not in campos_produtos:
        cursor.execute('ALTER TABLE produtos ADD COLUMN codigo TEXT DEFAULT ""')
    if 'marca' not in campos_produtos:
        cursor.execute('ALTER TABLE produtos ADD COLUMN marca TEXT DEFAULT ""')
    if 'status' not in campos_produtos:
        cursor.execute('ALTER TABLE produtos ADD COLUMN status TEXT DEFAULT "Estoque normal"')
    if 'criado_em' not in campos_produtos:
        cursor.execute('ALTER TABLE produtos ADD COLUMN criado_em TEXT DEFAULT CURRENT_TIMESTAMP')

    conn.commit()


def inserir_dados_padrao():
    inserir_categorias_padrao()
    inserir_produtos_padrao()
    inserir_usuarios_padrao()


def inserir_categorias_padrao():
    categorias_padrao = [
        'Informática',
        'Celulares',
        'Periféricos',
        'Redes',
        'Escritório',
        'Acessórios'
    ]
    with conectar_banco() as conn:
        cursor = conn.cursor()
        cursor.executemany('INSERT OR IGNORE INTO categorias (nome) VALUES (?)', [(categoria,) for categoria in categorias_padrao])
        conn.commit()


def inserir_produtos_padrao():
    produtos = [
        ('P-1001', 'Notebook Dell', 'Informática', 'Dell', 15, 5, 3500.00, 'Estoque normal'),
        ('P-1002', 'iPhone 13', 'Celulares', 'Apple', 8, 3, 5200.00, 'Estoque normal'),
        ('P-1003', 'Mouse Gamer', 'Periféricos', 'Logitech', 4, 5, 150.00, 'Atenção: Estoque baixo'),
        ('P-1004', 'Roteador TP-Link', 'Redes', 'TP-Link', 2, 3, 280.00, 'Crítico: Estoque muito baixo'),
        ('P-1005', 'Cadeira Escritório', 'Escritório', 'Newdesk', 10, 2, 900.00, 'Estoque normal'),
        ('P-1006', 'Carregador USB-C', 'Acessórios', 'Baseus', 20, 5, 80.00, 'Estoque normal')
    ]
    with conectar_banco() as conn:
        cursor = conn.cursor()
        cursor.executemany('''
            INSERT OR IGNORE INTO produtos
            (codigo, produto, categoria, marca, estoque_atual, estoque_minimo, preco, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', produtos)
        conn.commit()


def inserir_usuarios_padrao():
    senha_hash = generate_password_hash('admin123')
    with conectar_banco() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO usuarios
            (nome, username, email, cargo, senha, foto_perfil, criado_em)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            'Administrador',
            'admin',
            'admin@empresa.com',
            'Admin',
            senha_hash,
            '',
            datetime.utcnow().isoformat()
        ))
        conn.commit()
