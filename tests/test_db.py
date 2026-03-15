import sys; sys.path.insert(0, '.')
import pytest
from backend.app import app, db, User


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        admin = User(first_name='Admin', last_name='Test', login='admin_test', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
    with app.test_client() as c:
        yield c


def test_login_success(client):
    resp = client.post('/api/login', json={'login': 'admin_test', 'password': 'admin123'})
    assert resp.status_code == 200
    assert resp.json['role'] == 'admin'


def test_login_wrong_password(client):
    resp = client.post('/api/login', json={'login': 'admin_test', 'password': 'wrong'})
    assert resp.status_code == 401


def test_create_user_as_admin(client):
    client.post('/api/login', json={'login': 'admin_test', 'password': 'admin123'})
    resp = client.post('/api/admin/create_user', json={
        'first_name': 'Иван', 'last_name': 'Иванов',
        'login': 'ivan', 'password': 'pass123', 'role': 'user'
    })
    assert resp.status_code == 201


def test_create_user_duplicate_login(client):
    client.post('/api/login', json={'login': 'admin_test', 'password': 'admin123'})
    data = {'first_name': 'A', 'last_name': 'B', 'login': 'dup', 'password': '1', 'role': 'user'}
    client.post('/api/admin/create_user', json=data)
    resp = client.post('/api/admin/create_user', json=data)
    assert resp.status_code == 400
