def listar_categorias(conn):
    """Lista todas as categorias ordenadas alfabeticamente."""
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome FROM categorias ORDER BY nome ASC')
    return [dict(row) for row in cursor.fetchall()]


def adicionar_categoria(conn, nome):
    """Adiciona uma nova categoria."""
    if not nome or not nome.strip():
        raise ValueError('Nome da categoria é obrigatório')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO categorias (nome) VALUES (?)', (nome.strip(),))
    conn.commit()
    if cursor.rowcount == 0:
        raise ValueError('Categoria já existe')
    return cursor.lastrowid


def obter_categoria(conn, categoria_id):
    """Obtém uma categoria específica por ID."""
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome FROM categorias WHERE id = ?', (categoria_id,))
    result = cursor.fetchone()
    if not result:
        raise ValueError('Categoria não encontrada')
    return dict(result)


def atualizar_categoria(conn, categoria_id, nome):
    """Atualiza o nome de uma categoria."""
    if not nome or not nome.strip():
        raise ValueError('Nome da categoria é obrigatório')
    cursor = conn.cursor()
    cursor.execute('UPDATE categorias SET nome = ? WHERE id = ?', (nome.strip(), categoria_id))
    conn.commit()
    if cursor.rowcount == 0:
        raise ValueError('Categoria não encontrada')
    return obter_categoria(conn, categoria_id)


def deletar_categoria(conn, categoria_id):
    """Deleta uma categoria."""
    cursor = conn.cursor()
    # Verifica se há produtos na categoria
    cursor.execute('SELECT COUNT(*) AS total FROM produtos WHERE categoria = (SELECT nome FROM categorias WHERE id = ?)', (categoria_id,))
    if cursor.fetchone()['total'] > 0:
        raise ValueError('Não é possível deletar categoria com produtos')
    
    cursor.execute('DELETE FROM categorias WHERE id = ?', (categoria_id,))
    conn.commit()
    if cursor.rowcount == 0:
        raise ValueError('Categoria não encontrada')


def contar_produtos_por_categoria(conn):
    """Retorna contagem de produtos por categoria."""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.id, c.nome, COUNT(p.id) AS total_produtos
        FROM categorias c
        LEFT JOIN produtos p ON p.categoria = c.nome
        GROUP BY c.id, c.nome
        ORDER BY total_produtos DESC
    ''')
    return [dict(row) for row in cursor.fetchall()]


def obter_estatisticas_categorias(conn):
    """Retorna estatísticas completas de categorias."""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            c.id, 
            c.nome,
            COUNT(p.id) AS total_produtos,
            COALESCE(SUM(p.estoque_atual), 0) AS estoque_total,
            COALESCE(SUM(p.estoque_atual * p.preco), 0) AS valor_total
        FROM categorias c
        LEFT JOIN produtos p ON p.categoria = c.nome
        GROUP BY c.id, c.nome
        ORDER BY valor_total DESC
    ''')
    return [dict(row) for row in cursor.fetchall()]
