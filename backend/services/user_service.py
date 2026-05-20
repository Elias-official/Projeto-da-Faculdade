from werkzeug.security import generate_password_hash, check_password_hash

def criar_usuario(conn, data):
    username = data.get('username')
    senha = data.get('senha')

    if not username or not senha:
        raise ValueError('username e senha são obrigatórios')

    senha_hash = generate_password_hash(senha)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO usuarios (username, senha) VALUES (?, ?)', (username, senha_hash))
    conn.commit()
    return cursor.lastrowid

def autenticar_usuario(conn, username, senha):
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, senha FROM usuarios WHERE username = ?', (username,))
    row = cursor.fetchone()
    if not row:
        return None

    user_id, user_name, senha_hash = row
    if check_password_hash(senha_hash, senha):
        return {'id': user_id, 'username': user_name}

    return None

def listar_usuarios(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT id, username FROM usuarios')
    rows = cursor.fetchall()
    return [dict(row) for row in rows]
