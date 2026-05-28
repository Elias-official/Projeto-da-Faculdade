from flask import Blueprint, jsonify, request
from backend.database.db import conectar_banco
from backend.services.produto_service import adicionar_produto

produtos_bp = Blueprint('produtos', __name__)


@produtos_bp.route('/produtos', methods=['POST'])
def cadastrar_produto():
    dados = request.get_json() or {}

    try:
        with conectar_banco() as conn:
            produto_id = adicionar_produto(conn, dados)

        return jsonify({
            'mensagem': 'Produto cadastrado com sucesso!',
            'id': produto_id
        }), 201

    except ValueError as e:
        return jsonify({'erro': str(e)}), 400