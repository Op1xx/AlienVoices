from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox)


class AdminWindow(QWidget):
    def __init__(self, session, user):
        super().__init__()
        self.session = session
        self.user = user
        self.setWindowTitle(f"Администратор — {user['first_name']} {user['last_name']}")
        self.setMinimumSize(450, 400)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"{self.user['first_name']} {self.user['last_name']}"))
        layout.addWidget(QLabel("Роль: Администратор"))
        layout.addWidget(QLabel("─" * 40))
        layout.addWidget(QLabel("Создать нового пользователя"))

        form = QFormLayout()

        self.first_name = QLineEdit()
        self.last_name  = QLineEdit()
        self.login_inp  = QLineEdit()
        self.pass_inp   = QLineEdit()
        self.pass_inp.setEchoMode(QLineEdit.EchoMode.Password)
        self.role_combo = QComboBox()
        self.role_combo.addItems(['user', 'admin'])

        form.addRow("Имя:", self.first_name)
        form.addRow("Фамилия:", self.last_name)
        form.addRow("Логин:", self.login_inp)
        form.addRow("Пароль:", self.pass_inp)
        form.addRow("Роль:", self.role_combo)

        layout.addLayout(form)

        btn = QPushButton("Создать пользователя")
        btn.clicked.connect(self._create_user)
        layout.addWidget(btn)

        self.setLayout(layout)

    def _create_user(self):
        resp = self.session.post('http://localhost:5000/api/admin/create_user', json={
            'first_name': self.first_name.text(),
            'last_name':  self.last_name.text(),
            'login':      self.login_inp.text(),
            'password':   self.pass_inp.text(),
            'role':       self.role_combo.currentText()
        })
        if resp.status_code == 201:
            QMessageBox.information(self, "Готово", "Пользователь создан!")
            self.first_name.clear(); self.last_name.clear()
            self.login_inp.clear();  self.pass_inp.clear()
        else:
            QMessageBox.warning(self, "Ошибка", resp.json().get('error', 'Ошибка'))
