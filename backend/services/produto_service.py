def adicionar_produto(conn, data):
    cursor = conn.cursor()
    codigo = data.get('codigo')
    produto = data.get('produto')
    categoria = data.get('categoria')
    marca = data.get('marca', '')
    estoque_atual = data.get('estoque_atual')
    estoque_minimo = data.get('estoque_minimo')
    preco = data.get('preco')

    if not codigo or not produto or not categoria or estoque_atual is None or estoque_minimo is None or preco is None:
        raise ValueError('Código, produto, categoria, estoque atual, estoque mínimo e preço são obrigatórios')

    status = definir_status_estoque(estoque_atual, estoque_minimo)
    cursor.execute('''
        INSERT INTO produtos (codigo, produto, categoria, marca, estoque_atual, estoque_minimo, preco, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (codigo, produto, categoria, marca, estoque_atual, estoque_minimo, preco, status))
    conn.commit()
    return cursor.lastrowid


def listar_produtos(conn, filtros=None):
    cursor = conn.cursor()
    query = 'SELECT * FROM produtos'
    conditions = []
    params = []

    if filtros:
        if filtros.get('search'):
            conditions.append('(codigo LIKE ? OR produto LIKE ? OR categoria LIKE ? OR marca LIKE ?)')
            q = f"%{filtros['search']}%"
            params.extend([q, q, q, q])
        if filtros.get('categoria'):
            conditions.append('categoria = ?')
            params.append(filtros['categoria'])
        if filtros.get('status'):
            conditions.append('status = ?')
            params.append(filtros['status'])

    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)

    query += ' ORDER BY produto ASC'
    if filtros and filtros.get('limit'):
        query += ' LIMIT ?'
        params.append(filtros['limit'])

    cursor.execute(query, params)
    rows = cursor.fetchall()
    return [dict(row) for row in rows]


def buscar_produto(conn, produto_id):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos WHERE id = ?', (produto_id,))
    row = cursor.fetchone()
    return dict(row) if row else None


def atualizar_produto(conn, produto_id, data):
    codigo = data.get('codigo')
    produto = data.get('produto')
    categoria = data.get('categoria')
    marca = data.get('marca', '')
    estoque_atual = data.get('estoque_atual')
    estoque_minimo = data.get('estoque_minimo')
    preco = data.get('preco')

    if not codigo or produto is None or categoria is None or estoque_atual is None or estoque_minimo is None or preco is None:
        raise ValueError('Todos os campos são obrigatórios para atualizar o produto')

    status = definir_status_estoque(estoque_atual, estoque_minimo)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE produtos
        SET codigo = ?, produto = ?, categoria = ?, marca = ?, estoque_atual = ?, estoque_minimo = ?, preco = ?, status = ?
        WHERE id = ?
    ''', (codigo, produto, categoria, marca, estoque_atual, estoque_minimo, preco, status, produto_id))
    conn.commit()
    return buscar_produto(conn, produto_id)


def deletar_produto(conn, produto_id):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM produtos WHERE id = ?', (produto_id,))
    conn.commit()
    return cursor.rowcount


def atualizar_estoque(conn, produto_id, quantidade, tipo):
    cursor = conn.cursor()
    cursor.execute('SELECT estoque_atual, estoque_minimo FROM produtos WHERE id = ?', (produto_id,))
    row = cursor.fetchone()
    if not row:
        raise ValueError('Produto não encontrado')

    estoque_atual = row['estoque_atual'] or 0
    if tipo == 'Entrada':
        estoque_atual += quantidade
    else:
        estoque_atual -= quantidade

    status = definir_status_estoque(estoque_atual, row['estoque_minimo'])
    cursor.execute('''
        UPDATE produtos
        SET estoque_atual = ?, status = ?
        WHERE id = ?
    ''', (estoque_atual, status, produto_id))
    conn.commit()
    return estoque_atual


def definir_status_estoque(estoque_atual, estoque_minimo):
    if estoque_atual <= 0:
        return 'Sem estoque'
    if estoque_atual <= 5:
        return 'Crítico: Estoque muito baixo'
    if estoque_atual <= estoque_minimo:
        return 'Atenção: Estoque baixo'
    return 'Estoque normal'
