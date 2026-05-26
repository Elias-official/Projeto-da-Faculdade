from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from database.db import conectar_banco
from services.user_service import autenticar_usuario, criar_usuario, buscar_usuario_por_id, atualizar_ultimo_login

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    dados = request.get_json() or {}
    usuario = dados.get('usuario') or dados.get('username') or dados.get('email') or dados.get('login')
    senha = dados.get('senha')

    if not usuario or not senha:
        return jsonify({'erro': 'Usuário ou senha são obrigatórios'}), 400

    with conectar_banco() as conn:
        user = autenticar_usuario(conn, usuario, senha)
        if not user:
            return jsonify({'erro': 'Usuário ou senha inválidos'}), 401
        atualizar_ultimo_login(conn, user['id'])

    token = create_access_token(identity=str(user['id']))
    return jsonify({'token': token, 'usuario': user}), 200


@auth_bp.route('/register', methods=['POST'])
def register():
    dados = request.get_json() or {}

    with conectar_banco() as conn:
        try:
            user_id = criar_usuario(conn, dados)
            return jsonify({'mensagem': 'Cadastro realizado com sucesso', 'id': user_id}), 201
        except ValueError as exc:
            return jsonify({'erro': str(exc)}), 400
        except Exception:
            return jsonify({'erro': 'Erro ao criar usuário'}), 500


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    with conectar_banco() as conn:
        user = buscar_usuario_por_id(conn, user_id)
    if not user:
        return jsonify({'erro': 'Usuário não encontrado'}), 404
    return jsonify(user), 200
