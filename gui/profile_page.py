from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class ProfilePage(QWidget):
    def __init__(self, user: dict):
        super().__init__()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(10)

        layout.addWidget(QLabel("Информация о пользователе"))
        layout.addWidget(QLabel(f"Имя: {user['first_name']}"))
        layout.addWidget(QLabel(f"Фамилия: {user['last_name']}"))
        layout.addWidget(QLabel(f"Логин: {user['login']}"))
        layout.addWidget(QLabel(f"Роль: {user['role']}"))

        self.setLayout(layout)
