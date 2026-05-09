import os
from dotenv import load_dotenv
from flask import Flask, render_template
from routes.produtos import produtos_bp
from database.db import criar_tabela

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', '01994')

criar_tabela()

app.register_blueprint(produtos_bp)

@app.route('/')
def homepage():
    return render_template('homepage.html')


if __name__ == "__main__":
    app.run(debug=True)