import os
import database.db as db
from database.db import criar_tabelas, inserir_dados_padrao

print('module DB_PATH:', db.DB_PATH)
print('__file__', db.__file__)
print('cwd', os.getcwd())
print('exists DB_PATH', os.path.exists(db.DB_PATH))
print('size DB_PATH', os.path.getsize(db.DB_PATH) if os.path.exists(db.DB_PATH) else 'n/a')

criar_tabelas()
print('after criar_tabelas size', os.path.getsize(db.DB_PATH) if os.path.exists(db.DB_PATH) else 'n/a')

import sqlite3
conn = sqlite3.connect(db.DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
print('tables after create:', cur.fetchall())
conn.close()
