import os
import sqlite3
from backend.database.db import criar_tabelas, inserir_dados_padrao

base = os.getcwd()
db_path = os.path.join(base, 'estoque.db')
if os.path.exists(db_path):
    os.remove(db_path)
    print('Arquivo antigo removido:', db_path)
else:
    print('Arquivo antigo não existia:', db_path)

criar_tabelas()
inserir_dados_padrao()
print('Banco recriado e seed aplicado')

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
print('Tables:', cur.fetchall())
cur.execute('SELECT id,username,email,senha FROM usuarios WHERE username=? OR email=?', ('admin','admin@empresa.com'))
row = cur.fetchone()
print('Admin row:', dict(row) if row else None)
conn.close()
