from flask import Blueprint, jsonify
from database.db import conectar_banco

produtos_bp = Blueprint('produtos', __name__)

@produtos_bp.route('/produtos', methods=['GET'])
def listar_produtos():
    # Aqui você pode adicionar a Lógica para Listar os Produtos

    produtos = [
        {
            "id": 1,
            "nome": "Produto 1",
            "quantidade": 15,
        },
        {
            "id": 2,
            "nome": "Produto 2",
            "quantidade": 30,
        }
    ]

    return jsonify(produtos)    