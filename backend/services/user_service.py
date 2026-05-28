from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

def criar_usuario(conn, data):
    nome = data.get('nome', '')
    username = data.get('username')
    email = data.get('email')
    cargo = data.get('cargo', 'Funcionário')
    senha = data.get('senha')

    if not nome or not username or not senha or not email:
        raise ValueError('Nome, usuário, e-mail e senha são obrigatórios')

    senha_hash = generate_password_hash(senha)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO usuarios (nome, username, email, cargo, senha, foto_perfil, criado_em)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (nome, username, email, cargo, senha_hash, '', datetime.utcnow().isoformat()))
    conn.commit()
    return cursor.lastrowid


def autenticar_usuario(conn, usuario, senha):
    if not usuario or not senha:
        return None

    usuario_normalizado = usuario.strip()
    cursor = conn.cursor()
    cursor.execute(
        '''
        SELECT * FROM usuarios
        WHERE LOWER(username) = LOWER(?) OR LOWER(email) = LOWER(?)
        ''',
        (usuario_normalizado, usuario_normalizado)
    )
    row = cursor.fetchone()
    if not row:
        return None

    if check_password_hash(row['senha'], senha):
        return {
            'id': row['id'],
            'nome': row['nome'],
            'usuario': row['username'],
            'email': row['email'],
            'cargo': row['cargo'],
            'foto_perfil': row['foto_perfil'] or '',
            'ultimo_login': row['ultimo_login'],
            'criado_em': row['criado_em']
        }

    return None


def buscar_usuario_por_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, username AS usuario, email, cargo, foto_perfil, criado_em, ultimo_login FROM usuarios WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    return dict(row) if row else None


def listar_usuarios(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, username AS usuario, email, cargo, foto_perfil, criado_em, ultimo_login FROM usuarios')
    return [dict(row) for row in cursor.fetchall()]


def atualizar_usuario(conn, user_id, data):
    fields = []
    params = []
    for key in ['nome', 'username', 'email', 'cargo', 'foto_perfil']:
        if key in data:
            fields.append(f"{key} = ?")
            params.append(data[key])
    if 'senha' in data:
        fields.append('senha = ?')
        params.append(generate_password_hash(data['senha']))
    if not fields:
        raise ValueError('Nenhum campo para atualizar')
    params.append(user_id)
    cursor = conn.cursor()
    cursor.execute(f'UPDATE usuarios SET {", ".join(fields)} WHERE id = ?', params)
    conn.commit()
    return buscar_usuario_por_id(conn, user_id)


def deletar_usuario(conn, user_id):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM usuarios WHERE id = ?', (user_id,))
    conn.commit()
    return cursor.rowcount


def atualizar_ultimo_login(conn, user_id):
    cursor = conn.cursor()
    cursor.execute('UPDATE usuarios SET ultimo_login = ? WHERE id = ?', (datetime.now(timezone.utc).isoformat(), user_id))
    conn.commit()
