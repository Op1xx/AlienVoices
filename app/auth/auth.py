import hashlib
import os
import sqlite3
from config import DATABASE_PATH


def _hash_password(password: str, salt: str) -> str:
    return hashlib.md5((salt + password).encode()).hexdigest()


def _generate_salt() -> str:
    return os.urandom(16).hex()


def register_user(username: str, password: str) -> bool:
    salt = _generate_salt()
    password_hash = _hash_password(password, salt)
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            conn.execute(
                "INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
                (username, password_hash, salt),
            )
        return True
    except sqlite3.IntegrityError:
        return False


def authenticate_user(username: str, password: str) -> bool:
    with sqlite3.connect(DATABASE_PATH) as conn:
        row = conn.execute(
            "SELECT password_hash, salt FROM users WHERE username = ?",
            (username,),
        ).fetchone()
    if row is None:
        return False
    stored_hash, salt = row
    return _hash_password(password, salt) == stored_hash
