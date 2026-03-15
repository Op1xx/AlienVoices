from PyQt6.QtWidgets import (QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt


class LoginWindow(QWidget):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.setWindowTitle("Вход в систему")
        self.setFixedSize(400, 250)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(12)

        layout.addWidget(QLabel("Классификатор сигналов"))

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")
        layout.addWidget(self.login_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        btn = QPushButton("Войти")
        btn.clicked.connect(self._do_login)
        layout.addWidget(btn)

        self.setLayout(layout)

    def _do_login(self):
        resp = self.session.post('http://localhost:5000/api/login', json={
            'login': self.login_input.text(),
            'password': self.password_input.text()
        })
        if resp.status_code == 200:
            user = resp.json()
            self.close()
            if user['role'] == 'admin':
                from gui.admin_window import AdminWindow
                self._next = AdminWindow(self.session, user)
            else:
                from gui.user_window import UserWindow
                self._next = UserWindow(self.session, user)
            self._next.show()
        else:
            QMessageBox.warning(self, "Ошибка", resp.json().get('error', 'Ошибка входа'))
