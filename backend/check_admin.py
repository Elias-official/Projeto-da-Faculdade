import os
import sqlite3
from werkzeug.security import check_password_hash
DB_PATH = os.path.join(os.getcwd(), 'database', 'estoque.db')
print('DB path:', DB_PATH)
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()
cur.execute('SELECT id, nome, username, email, cargo, senha FROM usuarios WHERE username=? OR email=?', ('admin','admin@empresa.com'))
row = cur.fetchone()
print('admin row:', dict(row) if row else None)
if row:
    print('admin123 valid:', check_password_hash(row['senha'], 'admin123'))
conn.close()
