from flask import Blueprint, jsonify, request
from database.db import conectar_banco

produtos_bp = Blueprint('produtos', __name__)

# LISTAR PRODUTOS

@produtos_bp.route('/produtos', methods=['GET'])
def listar_produtos():
    # Aqui você pode adicionar a Lógica para Listar os Produtos
    conexao, cursor = conectar_banco()

    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()

    conexao.close()

    lista_produtos = []

    for produto in produtos:
        lista_produtos.append({
            'id': produto[0],
            'nome': produto[1],
            'categoria': produto[2],
            'quantidade': produto[3],
            'estoque_minimo': produto[4],
            'preco': produto[5]
        })

    return jsonify(lista_produtos)

# CADASTRAR PRODUTO 

@produtos_bp.route('/produtos', methods=['POST'])
def cadastrar_produto():

    dados = request.json
    
    nome = dados.get('nome')
    categoria = dados.get('categoria')
    quantidade = dados.get('quantidade')
    estoque_minimo = dados.get('estoque_minimo')
    preco = dados.get('preco')

    conexao, cursor = conectar_banco()

    cursor.execute('''
        INSERT INTO produtos 
        (nome, categoria, quantidade, estoque_minimo, preco)
        VALUES (?, ?, ?, ?, ?)
    ''', (nome, categoria, quantidade, estoque_minimo, preco))

    conexao.commit()
    conexao.close()

    return jsonify({'mensagem': 'Produto cadastrado com sucesso!'}), 201