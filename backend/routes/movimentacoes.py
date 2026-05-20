from flask import Blueprint, request, jsonify
from database.db import conectar_banco
from services.movimentacao_service import adicionar_movimentacao, listar_movimentacoes

movimentacoes_bp = Blueprint('movimentacoes', __name__)


@movimentacoes_bp.route('/movimentacoes', methods=['POST'])
def criar_movimentacao():
    dados = request.get_json() or {}
    try:
        with conectar_banco() as conn:
            mov_id = adicionar_movimentacao(conn, dados)

        return jsonify({'mensagem': 'Movimentação criada', 'id': mov_id}), 201
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception:
        return jsonify({'erro': 'Erro ao criar movimentação'}), 500


@movimentacoes_bp.route('/movimentacoes', methods=['GET'])
def listar():
    with conectar_banco() as conn:
        movs = listar_movimentacoes(conn)
    return jsonify(movs), 200
