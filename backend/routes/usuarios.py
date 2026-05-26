from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from database.db import conectar_banco
from services.user_service import criar_usuario, listar_usuarios, buscar_usuario_por_id, atualizar_usuario, deletar_usuario

usuarios_bp = Blueprint('usuarios', __name__)


@usuarios_bp.route('/usuarios', methods=['GET'])
@jwt_required()
def listar():
    with conectar_banco() as conn:
        usuarios = listar_usuarios(conn)
    return jsonify(usuarios), 200


@usuarios_bp.route('/usuarios', methods=['POST'])
@jwt_required()
def criar():
    dados = request.get_json() or {}
    try:
        with conectar_banco() as conn:
            user_id = criar_usuario(conn, dados)
        return jsonify({'mensagem': 'Usuário criado', 'id': user_id}), 201
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception:
        return jsonify({'erro': 'Erro ao criar usuário'}), 500


@usuarios_bp.route('/usuarios/<int:user_id>', methods=['PUT'])
@jwt_required()
def editar_usuario(user_id):
    dados = request.get_json() or {}
    try:
        with conectar_banco() as conn:
            usuario = atualizar_usuario(conn, user_id, dados)
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
        return jsonify({'mensagem': 'Usuário atualizado com sucesso', 'usuario': usuario}), 200
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception:
        return jsonify({'erro': 'Erro ao atualizar usuário'}), 500


@usuarios_bp.route('/usuarios/<int:user_id>', methods=['DELETE'])
@jwt_required()
def remover_usuario(user_id):
    with conectar_banco() as conn:
        total = deletar_usuario(conn, user_id)
    if total == 0:
        return jsonify({'erro': 'Usuário não encontrado'}), 404
    return jsonify({'mensagem': 'Usuário removido'}), 200

