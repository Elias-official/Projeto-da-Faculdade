def adicionar_movimentacao(conn, data):
    produto_id = data.get('produto_id')
    tipo = data.get('tipo')
    quantidade = data.get('quantidade')
    data_movimentacao = data.get('data_movimentacao')

    if not produto_id or not tipo or quantidade is None or not data_movimentacao:
        raise ValueError('produto_id, tipo, quantidade e data_movimentacao são obrigatórios')

    cursor = conn.cursor()
    cursor.execute('INSERT INTO movimentacoes (produto_id, tipo, quantidade, data_movimentacao) VALUES (?, ?, ?, ?)',
                   (produto_id, tipo, quantidade, data_movimentacao))
    conn.commit()
    return cursor.lastrowid

def listar_movimentacoes(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT id, produto_id, tipo, quantidade, data_movimentacao FROM movimentacoes')
    rows = cursor.fetchall()
    return [dict(row) for row in rows]
