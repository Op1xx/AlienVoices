import os
import sqlite3
import pytest
import config
from app.database.models import init_db
from app.auth.auth import register_user, authenticate_user

TEST_DB = "/tmp/alienvoices_test.db"


@pytest.fixture(autouse=True)
def use_test_db(monkeypatch, tmp_path):
    db = str(tmp_path / "test.db")
    monkeypatch.setattr(config, "DATABASE_PATH", db)
    import app.auth.auth as auth_module
    import app.database.models as models_module
    monkeypatch.setattr(auth_module, "DATABASE_PATH", db)
    monkeypatch.setattr(models_module, "DATABASE_PATH", db)
    init_db()


def test_register_and_login():
    assert register_user("mikhail", "secret") is True
    assert authenticate_user("mikhail", "secret") is True


def test_wrong_password():
    register_user("mikhail", "secret")
    assert authenticate_user("mikhail", "wrong") is False


def test_duplicate_register():
    register_user("mikhail", "secret")
    assert register_user("mikhail", "other") is False
