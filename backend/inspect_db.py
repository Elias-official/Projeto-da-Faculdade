import sqlite3
import os

BASE_DIR = os.getcwd()
DB_PATH = os.path.join(BASE_DIR, 'estoque.db')
print('DB path:', DB_PATH)
print('exists', os.path.exists(DB_PATH))
print('size', os.path.getsize(DB_PATH) if os.path.exists(DB_PATH) else 'N/A')
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print('tables:', cursor.fetchall())
try:
    cursor.execute('SELECT id,nome,username,email,cargo,senha,criado_em FROM usuarios WHERE username=? OR email=?', ('admin','admin@empresa.com'))
    row = cursor.fetchone()
    print('admin row:', dict(row) if row else None)
except Exception as e:
    print('error querying users:', e)
conn.close()
