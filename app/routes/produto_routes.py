from flask import Blueprint, jsonify, request
from database.db import conectar_banco
from services.produto_service import adicionar_produto

produtos_bp = Blueprint('produtos', __name__)

@produtos_bp.route('/produtos', methods=['POST'])
def cadastrar_produto():
    dados = request.json

    conexao, cursor = conectar_banco()

    adicionar_produto(
        cursor,
        dados['nome'],
        dados['categoria'],
        dados['quantidade'],
        dados['preco'],
        dados['estoque_minimo']
    )

    conexao.commit()
    conexao.close()

    return jsonify({
        "mensagem": "Produto cadastrado com sucesso"
    }),201