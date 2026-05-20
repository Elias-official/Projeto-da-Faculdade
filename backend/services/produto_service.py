def adicionar_produto(conn, data):
    cursor = conn.cursor()
    
    produto = data.get('produto')
    categoria = data.get('categoria')
    estoque_atual = data.get('estoque_atual')
    estoque_minimo = data.get('estoque_minimo')
    preco = data.get('preco')
    
    if not produto or not categoria or estoque_atual is None or estoque_minimo is None or preco is None:
        raise ValueError("Produto, categoria, estoque atual, estoque mínimo e preço são obrigatórios")
    
    status = definir_status_estoque(estoque_atual, estoque_minimo)


    cursor.execute('''
        INSERT INTO produtos 
        (
            produto, 
            categoria, 
            estoque_atual, 
            estoque_minimo, 
            preco,
            status
        )
        
        VALUES (?, ?, ?, ?, ?, ?)
            
    ''', (
            produto, 
            categoria, 
            estoque_atual, 
            estoque_minimo, 
            preco,
            status
        ))
   
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

def definir_status_estoque(estoque_atual, estoque_minimo):
    if estoque_atual <= 5:
        return 'Crítico: Estoque muito baixo'
    elif estoque_atual <= estoque_minimo:
        return 'Atenção: Estoque baixo'
    else:
        return 'Estoque normal'