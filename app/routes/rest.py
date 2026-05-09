from flask import Blueprint, jsonify, request
from database.db import conectar_banco
from services.produto_service import adicionar_produto, listar_produtos, deletar_produto

produtos_bp = Blueprint('produtos', __name__)

@produtos_bp.route('/produtos', methods=['POST'])
def create():
    data = request.get_json()

    if not data:
        return jsonify({"erro": "JSON inválido"}), 400

    try:
        with conectar_banco() as conn:
            produto_id = adicionar_produto(conn, data)

        return jsonify({
            "mensagem": "Produto cadastrado com sucesso",
            "id": produto_id
        }), 201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

@produtos_bp.route('/produtos', methods=['GET'])
def get_all():
    with conectar_banco() as conn:
        produtos = listar_produtos(conn)

    return jsonify(produtos), 200

@produtos_bp.route('/produtos/<int:produto_id>', methods=['DELETE'])
def delete(produto_id):
    with conectar_banco() as conn:
        rows_deleted = deletar_produto(conn, produto_id)

    if rows_deleted == 0:
        return jsonify({"erro": "Produto não encontrado"}), 404

    return jsonify({"mensagem": "Produto deletado com sucesso"}), 200
