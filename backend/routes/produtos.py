from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from database.db import conectar_banco
from services.produto_service import (
    adicionar_produto,
    listar_produtos,
    buscar_produto,
    atualizar_produto,
    deletar_produto,
)
from services.report_service import dashboard_resumo, categorias_por_produto, movimentacoes_por_tipo

produtos_bp = Blueprint('produtos', __name__)


@produtos_bp.route('/produtos', methods=['GET'])
@jwt_required()
def listar_produtos_route():
    filtros = {
        'search': request.args.get('search'),
        'categoria': request.args.get('categoria'),
        'status': request.args.get('status'),
        'page': request.args.get('page', 1, type=int),
        'limit': request.args.get('limit', 100, type=int)
    }
    with conectar_banco() as conexao:
        produtos = listar_produtos(conexao, filtros)
    return jsonify(produtos)


@produtos_bp.route('/produtos/<int:produto_id>', methods=['GET'])
@jwt_required()
def obter_produto(produto_id):
    with conectar_banco() as conexao:
        produto = buscar_produto(conexao, produto_id)
    if not produto:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    return jsonify(produto)


@produtos_bp.route('/produtos', methods=['POST'])
@jwt_required()
def cadastrar_produto():
    dados = request.get_json() or {}
    try:
        with conectar_banco() as conexao:
            produto_id = adicionar_produto(conexao, dados)
        return jsonify({'mensagem': 'Produto cadastrado com sucesso!', 'id': produto_id}), 201
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception:
        return jsonify({'erro': 'Erro ao cadastrar produto'}), 500


@produtos_bp.route('/produtos/<int:produto_id>', methods=['PUT'])
@jwt_required()
def editar_produto(produto_id):
    dados = request.get_json() or {}
    try:
        with conectar_banco() as conexao:
            produto = atualizar_produto(conexao, produto_id, dados)
        if not produto:
            return jsonify({'erro': 'Produto não encontrado'}), 404
        return jsonify({'mensagem': 'Produto atualizado com sucesso!', 'produto': produto}), 200
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception:
        return jsonify({'erro': 'Erro ao atualizar produto'}), 500


@produtos_bp.route('/produtos/<int:produto_id>', methods=['DELETE'])
@jwt_required()
def remover_produto(produto_id):
    with conectar_banco() as conexao:
        total = deletar_produto(conexao, produto_id)
    if total == 0:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    return jsonify({'mensagem': 'Produto removido'}), 200


@produtos_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    with conectar_banco() as conexao:
        data = dashboard_resumo(conexao)
    return jsonify(data)


@produtos_bp.route('/grafico/categorias', methods=['GET'])
@jwt_required()
def grafico_categorias():
    with conectar_banco() as conexao:
        data = categorias_por_produto(conexao)
    return jsonify(data)


@produtos_bp.route('/grafico/movimentacoes', methods=['GET'])
@jwt_required()
def grafico_movimentacoes():
    with conectar_banco() as conexao:
        data = movimentacoes_por_tipo(conexao)
    return jsonify(data)
 