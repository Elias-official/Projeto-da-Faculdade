import os
from dotenv import load_dotenv
from flask import Flask
from routes.rest import produtos_bp
from database.db import conectar_banco, criar_tabela, inserir_produtos_padrao

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '01994')

app.register_blueprint(produtos_bp)

criar_tabela()

if __name__ == "__main__":
    app.run(debug=True)

