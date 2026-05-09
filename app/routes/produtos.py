from flask import Blueprint, jsonify, request
from database.db import conectar_banco

produtos_bp = Blueprint('produtos', __name__)

# LISTAR PRODUTOS

@produtos_bp.route('/produtos', methods=['GET'])
def listar_produtos():
    conexao = conectar_banco()
    cursor = conexao.cursor()

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

    if not nome:
        return jsonify({
        "erro": "Nome obrigatório"
    }), 400

    if quantidade <= 0:
        return jsonify({
        "erro": "Produto sem estoque"
    }), 400

    if preco <= 0:
        return jsonify({
        "erro": "Preço inválido"
    }), 400

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute('''
        INSERT INTO produtos 
        (nome, categoria, quantidade, estoque_minimo, preco)
        VALUES (?, ?, ?, ?, ?)
    ''', (nome, categoria, quantidade, estoque_minimo, preco))

    conexao.commit()
    conexao.close()
    
    return jsonify({'mensagem': 'Produto cadastrado com sucesso!'}), 201