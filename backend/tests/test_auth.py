import backend.database.db as db
from backend.app import create_app


def test_admin_login_by_username_and_email(tmp_path):
    db.DB_PATH = str(tmp_path / 'test_estoque.db')
    app = create_app()

    with app.test_client() as client:
        for attempt in range(10):
            usuario = 'admin' if attempt % 2 == 0 else 'admin@empresa.com'
            response = client.post('/login', json={'usuario': usuario, 'senha': 'admin123'})
            assert response.status_code == 200, f'Attempt {attempt} failed with {response.status_code} {response.data}'
            assert 'token' in response.json
            assert response.json['usuario']['usuario'] == 'admin'


def test_admin_login_is_case_insensitive_for_username_and_email(tmp_path):
    db.DB_PATH = str(tmp_path / 'test_estoque_case.db')
    app = create_app()

    with app.test_client() as client:
        response = client.post('/login', json={'usuario': 'ADMIN', 'senha': 'admin123'})
        assert response.status_code == 200
        assert response.json['usuario']['usuario'] == 'admin'

        response = client.post('/login', json={'usuario': 'Admin@Empresa.Com', 'senha': 'admin123'})
        assert response.status_code == 200
        assert response.json['usuario']['usuario'] == 'admin'


def test_admin_login_rejects_wrong_password(tmp_path):
    db.DB_PATH = str(tmp_path / 'test_estoque_wrong.db')
    app = create_app()

    with app.test_client() as client:
        response = client.post('/login', json={'usuario': 'admin', 'senha': 'senhaerrada'})
        assert response.status_code == 401
        assert response.json['erro'] == 'Usuário ou senha inválidos'
