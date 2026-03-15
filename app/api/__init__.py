from flask import Flask
from config import SECRET_KEY


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = SECRET_KEY

    from .routes import bp
    app.register_blueprint(bp)

    return app
