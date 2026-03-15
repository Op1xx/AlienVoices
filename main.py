import sys
from app.database.models import init_db


def run_gui():
    from app.gui.main_window import run_app
    run_app()


def run_api():
    from app.api import create_app
    app = create_app()
    from config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)


if __name__ == "__main__":
    init_db()

    mode = sys.argv[1] if len(sys.argv) > 1 else "gui"

    if mode == "api":
        run_api()
    else:
        run_gui()
