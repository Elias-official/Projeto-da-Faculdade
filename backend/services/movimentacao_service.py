from datetime import datetime
from .produto_service import atualizar_estoque

def adicionar_movimentacao(conn, data):
    produto_id = data.get('produto_id')
    tipo = data.get('tipo')
    quantidade = data.get('quantidade')
    usuario_id = data.get('usuario_id')
    data_movimentacao = data.get('data_movimentacao') or datetime.utcnow().isoformat()

    if not produto_id or not tipo or quantidade is None or not usuario_id:
        raise ValueError('produto_id, tipo, quantidade e usuário são obrigatórios')

    if tipo not in ('Entrada', 'Saída'):
        raise ValueError('Tipo de movimentação inválido. Use Entrada ou Saída')

    estoque_atualizado = atualizar_estoque(conn, produto_id, quantidade, tipo)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO movimentacoes (produto_id, usuario_id, tipo, quantidade, data_movimentacao) VALUES (?, ?, ?, ?, ?)',
        (produto_id, usuario_id, tipo, quantidade, data_movimentacao)
    )
    conn.commit()
    return cursor.lastrowid


def listar_movimentacoes(conn):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT m.id, m.produto_id, p.produto AS nome_produto, m.tipo, m.quantidade, m.data_movimentacao, m.usuario_id
        FROM movimentacoes m
        LEFT JOIN produtos p ON p.id = m.produto_id
        ORDER BY m.data_movimentacao DESC
    ''')
    rows = cursor.fetchall()
    return [dict(row) for row in rows]
