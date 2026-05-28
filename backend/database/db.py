import os
import sqlite3
from datetime import datetime, timezone
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
                criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
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
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
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
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
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
        cursor.execute('ALTER TABLE produtos ADD COLUMN criado_em TEXT DEFAULT ""')
    if 'created_at' not in campos_produtos:
        cursor.execute('ALTER TABLE produtos ADD COLUMN created_at TEXT DEFAULT ""')

    conn.commit()

    # garantir colunas em usuarios
    cursor.execute("PRAGMA table_info(usuarios)")
    campos_usuarios = [row['name'] for row in cursor.fetchall()]
    if 'created_at' not in campos_usuarios:
        cursor.execute('ALTER TABLE usuarios ADD COLUMN created_at TEXT DEFAULT ""')
    if 'criado_em' not in campos_usuarios:
        cursor.execute('ALTER TABLE usuarios ADD COLUMN criado_em TEXT DEFAULT ""')

    # garantir colunas em movimentacoes
    cursor.execute("PRAGMA table_info(movimentacoes)")
    campos_mov = [row['name'] for row in cursor.fetchall()]
    if 'created_at' not in campos_mov:
        cursor.execute('ALTER TABLE movimentacoes ADD COLUMN created_at TEXT DEFAULT ""')

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
        ('P-1002', 'PC Gamer Ryzen', 'Informática', 'AMD', 7, 3, 6200.00, 'Estoque normal'),
        ('P-1003', 'SSD 1TB', 'Informática', 'Kingston', 12, 4, 450.00, 'Estoque normal'),
        ('P-1004', 'iPhone 13', 'Celulares', 'Apple', 8, 3, 5200.00, 'Estoque normal'),
        ('P-1005', 'Galaxy S23', 'Celulares', 'Samsung', 5, 2, 3800.00, 'Atenção: Estoque baixo'),
        ('P-1006', 'Xiaomi Redmi Note', 'Celulares', 'Xiaomi', 9, 4, 1750.00, 'Estoque normal'),
        ('P-1007', 'Mouse Gamer', 'Periféricos', 'Logitech', 4, 5, 150.00, 'Atenção: Estoque baixo'),
        ('P-1008', 'Teclado Mecânico', 'Periféricos', 'HyperX', 6, 3, 320.00, 'Estoque normal'),
        ('P-1009', 'Headset RGB', 'Periféricos', 'Razer', 3, 3, 420.00, 'Atenção: Estoque baixo'),
        ('P-1010', 'Roteador TP-Link', 'Redes', 'TP-Link', 2, 3, 280.00, 'Crítico: Estoque muito baixo'),
        ('P-1011', 'Switch 8 portas', 'Redes', 'D-Link', 5, 2, 360.00, 'Estoque normal'),
        ('P-1012', 'Access Point', 'Redes', 'Cisco', 4, 2, 760.00, 'Estoque normal'),
        ('P-1013', 'Cadeira Escritório', 'Escritório', 'Newdesk', 10, 2, 900.00, 'Estoque normal'),
        ('P-1014', 'Mesa Gamer', 'Escritório', 'Madesa', 3, 2, 1100.00, 'Atenção: Estoque baixo'),
        ('P-1015', 'Impressora Multifuncional', 'Escritório', 'HP', 6, 2, 650.00, 'Estoque normal'),
        ('P-1016', 'Carregador USB-C', 'Acessórios', 'Baseus', 20, 5, 80.00, 'Estoque normal'),
        ('P-1017', 'Cabo HDMI 2m', 'Acessórios', 'Belkin', 14, 4, 45.00, 'Estoque normal'),
        ('P-1018', 'Fone de Ouvido Bluetooth', 'Acessórios', 'JBL', 8, 3, 240.00, 'Estoque normal')
    ]
    produtos += gerar_produtos_empresariais(500)
    with conectar_banco() as conn:
        cursor = conn.cursor()
        cursor.executemany('''
            INSERT OR IGNORE INTO produtos
            (codigo, produto, categoria, marca, estoque_atual, estoque_minimo, preco, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', produtos)
        conn.commit()


def gerar_produtos_empresariais(total):
    categorias = [
        'Informática',
        'Celulares',
        'Periféricos',
        'Redes',
        'Escritório',
        'Acessórios'
    ]

    templates = {
        'Informática': [
            'Monitor LED', 'Fonte ATX', 'Placa de vídeo', 'Memória RAM', 'Cooler CPU',
            'Placa-mãe', 'Gabinete Gamer', 'Webcam Full HD', 'HD Externo', 'Dock Station',
            'Mouse pad XXL', 'Teclado Bluetooth', 'No-break 1200VA', 'Módulo Wi-Fi PCI', 'SSD NVMe 512GB'
        ],
        'Celulares': [
            'Carregador Turbo', 'Película de vidro', 'Smartwatch', 'Powerbank',
            'Capa Antichoque', 'Fone Bluetooth', 'Suporte para celular', 'Cabo Lightning',
            'Cabo USB-C', 'Bateria sobressalente', 'Película anti-reflexo', 'Base de carregamento', 'Capa magnética'
        ],
        'Periféricos': [
            'Mouse sem fio', 'Teclado slim', 'Alto-falante', 'Microfone USB',
            'Controle Gamer', 'Leitor de cartão', 'Hub USB', 'Base refrigerada',
            'Webcam 1080p', 'Teclado para notebook', 'Mesa digitalizadora', 'Fone gamer', 'Dock USB'
        ],
        'Redes': [
            'Patch Cord', 'Adaptador USB-Ethernet', 'Repetidor Wi-Fi', 'Câmera IP',
            'Switch PoE', 'Módulo SFP', 'Modem 4G', 'Splitter de rede',
            'Placa de rede', 'Extensor de alcance', 'Firewall appliance', 'Access Point indoor', 'Patch Panel'
        ],
        'Escritório': [
            'Bloco de notas', 'Pasta suspensa', 'Organizador de mesa', 'Luminária de mesa',
            'Scanner portátil', 'Calculadora financeira', 'Armário modular', 'Estante de livros',
            'Quadro branco', 'Cesto de lixo', 'Caneta stylus', 'Suporte para notebook', 'Agenda executiva'
        ],
        'Acessórios': [
            'Pen Drive 32GB', 'Cabo DisplayPort', 'Adaptador HDMI', 'Kit limpeza',
            'Base para celular', 'Carregador veicular', 'Cabo de força', 'Hub de carregamento',
            'Suporte para headset', 'Cabo VGA', 'Cartão de memória', 'Capa para fone', 'Alça para mala'
        ]
    }

    marcas = {
        'Informática': ['Corsair', 'Asus', 'Gigabyte', 'Kingston', 'Cooler Master'],
        'Celulares': ['Samsung', 'Apple', 'Xiaomi', 'Motorola', 'OnePlus'],
        'Periféricos': ['Logitech', 'Razer', 'HyperX', 'SteelSeries', 'Microsoft'],
        'Redes': ['TP-Link', 'D-Link', 'Cisco', 'Ubiquiti', 'Mikrotik'],
        'Escritório': ['HP', 'Epson', 'Newdesk', 'Faber-Castell', 'Samsung'],
        'Acessórios': ['Belkin', 'Anker', 'JBL', 'Baseus', 'Philips']
    }

    produtos = []
    codigo_inicial = 2000

    for index in range(total):
        categoria = categorias[index % len(categorias)]
        nomes = templates[categoria]
        nome_base = nomes[index % len(nomes)]
        variacao = (index // len(nomes)) % 4 + 1
        produto = f'{nome_base} {variacao}' if variacao > 1 else nome_base
        marca = marcas[categoria][index % len(marcas[categoria])]
        estoque_minimo = 2 + ((index % 5) * 2)
        estoque_atual = estoque_minimo + ((index % 12) - 3)
        if estoque_atual < 0:
            estoque_atual = 0
        if estoque_atual <= 1:
            status = 'Crítico: Estoque muito baixo'
        elif estoque_atual <= estoque_minimo:
            status = 'Atenção: Estoque baixo'
        else:
            status = 'Estoque normal'
        preco = round(60 + ((index * 37) % 4600) + (len(nome_base) % 12) * 4, 2)
        codigo = f'P-{codigo_inicial + index:04d}'
        produtos.append((codigo, produto, categoria, marca, estoque_atual, estoque_minimo, preco, status))

    return produtos


def inserir_usuarios_padrao():
    with conectar_banco() as conn:
        garantir_admin(conn)

def garantir_admin(conn):
    """Utility: garante que o usuário admin exista e tenha a senha 'admin123'."""
    senha_hash = generate_password_hash('admin123')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM usuarios WHERE username = ? OR email = ?', ('admin', 'admin@empresa.com'))
    row = cursor.fetchone()
    if row:
        cursor.execute('UPDATE usuarios SET senha = ? WHERE id = ?', (senha_hash, row['id']))
    else:
        cursor.execute('''
            INSERT INTO usuarios (nome, username, email, cargo, senha, foto_perfil, criado_em)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            'Administrador',
            'admin',
            'admin@empresa.com',
            'Admin',
            senha_hash,
            '',
            datetime.now(timezone.utc).isoformat()
        ))
    conn.commit()
