import os
from dotenv import load_dotenv
from flask import Flask, render_template
from routes.produtos import produtos_bp
from database.db import criar_tabela, inserir_produtos_padrao
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes.auth import auth_bp

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', '01994')
CORS(app)
app.config['JWT_SECRET_KEY'] = 'estoque_secret_key'
jwt = JWTManager(app)

criar_tabela()

inserir_produtos_padrao()

from database.db import inserir_usuarios_padrao

inserir_usuarios_padrao()

app.register_blueprint(produtos_bp)
app.register_blueprint(auth_bp)
from routes.usuarios import usuarios_bp

app.register_blueprint(usuarios_bp)
from routes.movimentacoes import movimentacoes_bp

app.register_blueprint(movimentacoes_bp)

@app.route('/')
def homepage():
    return render_template('homepage.html')


if __name__ == "__main__":
    app.run(debug=True)