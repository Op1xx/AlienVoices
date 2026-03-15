import sys; sys.path.insert(0, '.')
from backend.db import User


def test_password_hash_not_plain():
    u = User(first_name='Test', last_name='User', login='t', role='user')
    u.set_password('secret123')
    assert u.password_hash != 'secret123'


def test_password_check_correct():
    u = User(first_name='Test', last_name='User', login='t', role='user')
    u.set_password('mypassword')
    assert u.check_password('mypassword') is True


def test_password_check_wrong():
    u = User(first_name='Test', last_name='User', login='t', role='user')
    u.set_password('mypassword')
    assert u.check_password('wrongpassword') is False


def test_salt_is_unique():
    u1 = User(first_name='A', last_name='B', login='a', role='user')
    u2 = User(first_name='C', last_name='D', login='c', role='user')
    u1.set_password('same')
    u2.set_password('same')
    assert u1.salt != u2.salt
    assert u1.password_hash != u2.password_hash
