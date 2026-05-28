import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

load_dotenv()


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'estoque_secret_key')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'estoque_jwt_secret_default_2026_123456')
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

    CORS(app)
    JWTManager(app)

    from backend.database.db import criar_tabelas, inserir_dados_padrao
    criar_tabelas()
    inserir_dados_padrao()

    from backend.routes.auth import auth_bp
    from backend.routes.produtos import produtos_bp
    from backend.routes.movimentacoes import movimentacoes_bp
    from backend.routes.usuarios import usuarios_bp
    from backend.routes.categorias import categorias_bp
    from backend.routes.relatorios import relatorios_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(produtos_bp)
    app.register_blueprint(movimentacoes_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(categorias_bp)
    app.register_blueprint(relatorios_bp)

    @app.route('/')
    def status():
        return jsonify({'status': 'API de inventário em execução'})

    return app


if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)
