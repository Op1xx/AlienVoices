from flask import Flask, request, jsonify, session
from backend.db import db, User
from backend.predict import predict_npz
import numpy as np
import json
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Кэш результатов последнего теста (в памяти, на сессию)
_last_test_result = {}


def require_role(*roles):
    """Декоратор проверки роли"""
    from functools import wraps
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user_id = session.get('user_id')
            if not user_id:
                return jsonify({'error': 'Не авторизован'}), 401
            user = User.query.get(user_id)
            if not user or user.role not in roles:
                return jsonify({'error': 'Нет доступа'}), 403
            return f(*args, **kwargs)
        return wrapped
    return decorator


@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(login=data.get('login')).first()
    if not user or not user.check_password(data.get('password', '')):
        return jsonify({'error': 'Неверный логин или пароль'}), 401
    session['user_id'] = user.id
    return jsonify(user.to_dict())


@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'ok': True})


@app.route('/api/me', methods=['GET'])
def me():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Не авторизован'}), 401
    user = User.query.get(user_id)
    return jsonify(user.to_dict())


@app.route('/api/admin/create_user', methods=['POST'])
@require_role('admin')
def create_user():
    data = request.json
    required = ['first_name', 'last_name', 'login', 'password', 'role']
    if not all(k in data for k in required):
        return jsonify({'error': 'Заполните все поля'}), 400
    if User.query.filter_by(login=data['login']).first():
        return jsonify({'error': 'Логин уже занят'}), 400
    user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        login=data['login'],
        role=data.get('role', 'user')
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@app.route('/api/upload_test', methods=['POST'])
@require_role('user', 'admin')
def upload_test():
    global _last_test_result
    if 'file' not in request.files:
        return jsonify({'error': 'Файл не передан'}), 400
    npz_bytes = request.files['file'].read()
    try:
        result = predict_npz(npz_bytes)
        _last_test_result = result
        return jsonify({
            'accuracy': result['accuracy'],
            'loss': result['loss'],
            'num_records': result['num_records']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analytics/training', methods=['GET'])
@require_role('user', 'admin')
def analytics_training():
    with open('ml/history.json') as f:
        history = json.load(f)
    return jsonify(history)


@app.route('/api/analytics/train_distribution', methods=['GET'])
@require_role('user', 'admin')
def analytics_train_distribution():
    data = np.load('data/train_fixed.npz', allow_pickle=True)
    train_y = data['train_y'].astype(int)
    unique, counts = np.unique(train_y, return_counts=True)
    return jsonify({
        'labels': unique.tolist(),
        'counts': counts.tolist()
    })


@app.route('/api/analytics/valid_top5', methods=['GET'])
@require_role('user', 'admin')
def analytics_valid_top5():
    data = np.load('data/train_fixed.npz', allow_pickle=True)
    valid_y = data['valid_y'].astype(int)
    unique, counts = np.unique(valid_y, return_counts=True)
    idx = np.argsort(counts)[::-1][:5]
    return jsonify({
        'labels': unique[idx].tolist(),
        'counts': counts[idx].tolist()
    })


@app.route('/api/analytics/test_confidence', methods=['GET'])
@require_role('user', 'admin')
def analytics_test_confidence():
    if not _last_test_result:
        return jsonify({'error': 'Сначала загрузите тестовый датасет'}), 400
    return jsonify({
        'confidence': _last_test_result['confidence'],
        'correct': _last_test_result['correct'],
        'predictions': _last_test_result['predictions'],
        'true_labels': _last_test_result['true_labels']
    })


def create_default_admin():
    """Создаёт администратора по умолчанию при первом запуске"""
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(login='admin').first():
            admin = User(
                first_name='Михаил',
                last_name='Администратор',
                login='admin',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Создан администратор: admin / admin123")


if __name__ == '__main__':
    create_default_admin()
    app.run(port=5000, debug=True)
