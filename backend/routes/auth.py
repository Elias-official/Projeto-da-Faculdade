from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from database.db import conectar_banco
from services.user_service import autenticar_usuario

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    dados = request.get_json() or {}
    username = dados.get('username')
    senha = dados.get('senha')

    if not username or not senha:
        return jsonify({'erro': 'username e senha são obrigatórios'}), 400

    with conectar_banco() as conn:
        user = autenticar_usuario(conn, username, senha)

    if not user:
        return jsonify({'erro': 'Usuário ou senha inválidos'}), 401

    token = create_access_token(identity=user['username'])
    return jsonify({'token': token}), 200