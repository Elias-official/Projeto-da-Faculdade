from flask import Flask

def create_app():
    app = Flask(__name__)
    
    from produto_routes import produtos_bp
    app.register_blueprint(produtos_bp, url_prefix='/api')

    return app