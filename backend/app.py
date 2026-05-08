from flask import Flask
from routes.produtos import produtos_bp
from flask import render_template
from database.db import criar_tabela


app = Flask(__name__)
app.secret_key = '01994'

criar_tabela()

app.register_blueprint(produtos_bp)

@app.route('/')
def homepage():
    return render_template('homepage.html')


if __name__ == "__main__":
    app.run(debug=True)