def adicionar_produto(conn, data):
    cursor = conn.cursor()
    
    nome = data.get('nome')
    categoria = data.get('categoria')
    quantidade = data.get('quantidade')
    estoque_minimo = data.get('estoque_minimo')
    preco = data.get('preco')
    
    if not nome or quantidade is None or preco is None:
        raise ValueError("Nome, quantidade e preço são obrigatórios")
    
    cursor.execute('''
        INSERT INTO produtos 
        (nome, categoria, quantidade, estoque_minimo, preco)
        VALUES (?, ?, ?, ?, ?)
    ''', (nome, categoria, quantidade, estoque_minimo, preco))
   
    conn.commit()
    return cursor.lastrowid

def listar_produtos(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()

    return [dict(produto) for produto in produtos]


def deletar_produto(conn, produto_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
    conn.commit()
    return cursor.rowcount