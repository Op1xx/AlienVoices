import sys
import threading
import time
import requests
from PyQt6.QtWidgets import QApplication
from gui.login_window import LoginWindow


def start_flask():
    from backend.app import app, create_default_admin
    create_default_admin()
    app.run(port=5000, debug=False, use_reloader=False)


flask_thread = threading.Thread(target=start_flask, daemon=True)
flask_thread.start()

time.sleep(1)  # ждём старта Flask

app = QApplication(sys.argv)
session = requests.Session()

window = LoginWindow(session)
window.show()
sys.exit(app.exec())
