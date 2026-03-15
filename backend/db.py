from flask_sqlalchemy import SQLAlchemy
import hashlib
import os

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id            = db.Column(db.Integer, primary_key=True)
    first_name    = db.Column(db.String(100), nullable=False)
    last_name     = db.Column(db.String(100), nullable=False)
    login         = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    salt          = db.Column(db.String(64), nullable=False)
    role          = db.Column(db.String(20), nullable=False, default='user')
    # role: 'admin' или 'user'

    def set_password(self, raw_password: str):
        self.salt = os.urandom(16).hex()
        self.password_hash = hashlib.md5(
            (self.salt + raw_password).encode()
        ).hexdigest()

    def check_password(self, raw_password: str) -> bool:
        expected = hashlib.md5(
            (self.salt + raw_password).encode()
        ).hexdigest()
        return self.password_hash == expected

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'login': self.login,
            'role': self.role
        }
