from flask import Blueprint, request, jsonify
from database.db import conectar_banco
from services.user_service import criar_usuario, listar_usuarios

usuarios_bp = Blueprint('usuarios', __name__)


@usuarios_bp.route('/usuarios', methods=['POST'])
def criar():
    dados = request.get_json() or {}
    try:
        with conectar_banco() as conn:
            user_id = criar_usuario(conn, dados)

        return jsonify({'mensagem': 'Usuário criado', 'id': user_id}), 201
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': 'Erro ao criar usuário'}), 500


@usuarios_bp.route('/usuarios', methods=['GET'])
def listar():
    with conectar_banco() as conn:
        usuarios = listar_usuarios(conn)
    return jsonify(usuarios), 200
