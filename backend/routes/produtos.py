from flask import Blueprint, jsonify, request
from database.db import conectar_banco
from services.produto_service import adicionar_produto, listar_produtos, deletar_produto

produtos_bp = Blueprint('produtos', __name__)

# LISTAR PRODUTOS

@produtos_bp.route('/produtos', methods=['GET'])
def listar_produtos_route():
    with conectar_banco() as conexao:
        produtos = listar_produtos(conexao)

    return jsonify(produtos)

# CADASTRAR PRODUTO 

@produtos_bp.route('/produtos', methods=['POST'])
def cadastrar_produto():
    dados = request.json or {}

    try:
        with conectar_banco() as conexao:
            produto_id = adicionar_produto(conexao, dados)

        return jsonify({
            'mensagem': 'Produto cadastrado com sucesso!',
            'id': produto_id
        }), 201

    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    
@produtos_bp.route('/dashboard', methods=['GET'])
def dashboard():

    conexao = conectar_banco()

    cursor = conexao.cursor()

    # TOTAL PRODUTOS
    cursor.execute("SELECT COUNT(*) FROM produtos")

    total_produtos = cursor.fetchone()[0]

    # ESTOQUE TOTAL
    cursor.execute("SELECT SUM(estoque_atual) FROM produtos")

    estoque_total = cursor.fetchone()[0]

    # ESTOQUE BAIXO
    cursor.execute('''
        SELECT COUNT(*) FROM produtos
        WHERE estoque_atual <= estoque_minimo
    ''')

    estoque_baixo = cursor.fetchone()[0]

    # VALOR ESTOQUE
    cursor.execute('''
        SELECT SUM(estoque_atual * preco)
        FROM produtos
    ''')

    valor_estoque = cursor.fetchone()[0]

    conexao.close()

    return jsonify({

        'total_produtos': total_produtos,

        'estoque_total': estoque_total,

        'estoque_baixo': estoque_baixo,

        'valor_estoque': valor_estoque

    })  

@produtos_bp.route('/grafico/categorias', methods=['GET'])
def grafico_categorias():

    conexao = conectar_banco()

    cursor = conexao.cursor()

    cursor.execute('''
        SELECT categoria, COUNT(*) as total
        FROM produtos
        GROUP BY categoria
    ''')

    dados = cursor.fetchall()

    conexao.close()

    categorias = []

    for item in dados:

        categorias.append({

            'categoria': item[0],

            'total': item[1]
        })

    return jsonify(categorias) 