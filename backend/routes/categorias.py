from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from database.db import conectar_banco
from services.categoria_service import (
    listar_categorias,
    adicionar_categoria,
    obter_categoria,
    atualizar_categoria,
    deletar_categoria,
    contar_produtos_por_categoria,
    obter_estatisticas_categorias
)

categorias_bp = Blueprint('categorias', __name__)


@categorias_bp.route('/categorias', methods=['GET'])
def listar():
    """Lista todas as categorias."""
    with conectar_banco() as conn:
        categorias = listar_categorias(conn)
    return jsonify(categorias), 200


@categorias_bp.route('/categorias', methods=['POST'])
@jwt_required()
def criar_categoria():
    """Cria uma nova categoria."""
    dados = request.get_json() or {}
    nome = dados.get('nome')
    try:
        with conectar_banco() as conn:
            categoria_id = adicionar_categoria(conn, nome)
        return jsonify({'mensagem': 'Categoria criada com sucesso', 'id': categoria_id}), 201
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': 'Erro ao criar categoria'}), 500


@categorias_bp.route('/categorias/<int:categoria_id>', methods=['GET'])
def obter(categoria_id):
    """Obtém uma categoria específica."""
    try:
        with conectar_banco() as conn:
            categoria = obter_categoria(conn, categoria_id)
        return jsonify(categoria), 200
    except ValueError as e:
        return jsonify({'erro': str(e)}), 404
    except Exception:
        return jsonify({'erro': 'Erro ao obter categoria'}), 500


@categorias_bp.route('/categorias/<int:categoria_id>', methods=['PUT'])
@jwt_required()
def atualizar(categoria_id):
    """Atualiza uma categoria."""
    dados = request.get_json() or {}
    nome = dados.get('nome')
    try:
        with conectar_banco() as conn:
            categoria = atualizar_categoria(conn, categoria_id, nome)
        return jsonify({'mensagem': 'Categoria atualizada', 'categoria': categoria}), 200
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception:
        return jsonify({'erro': 'Erro ao atualizar categoria'}), 500


@categorias_bp.route('/categorias/<int:categoria_id>', methods=['DELETE'])
@jwt_required()
def deletar(categoria_id):
    """Deleta uma categoria."""
    try:
        with conectar_banco() as conn:
            deletar_categoria(conn, categoria_id)
        return jsonify({'mensagem': 'Categoria deletada com sucesso'}), 200
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception:
        return jsonify({'erro': 'Erro ao deletar categoria'}), 500


@categorias_bp.route('/categorias/contagem/produtos', methods=['GET'])
def contar_produtos():
    """Retorna contagem de produtos por categoria."""
    with conectar_banco() as conn:
        dados = contar_produtos_por_categoria(conn)
    return jsonify(dados), 200


@categorias_bp.route('/categorias/estatisticas/completo', methods=['GET'])
def estatisticas():
    """Retorna estatísticas completas de categorias."""
    with conectar_banco() as conn:
        dados = obter_estatisticas_categorias(conn)
    return jsonify(dados), 200
