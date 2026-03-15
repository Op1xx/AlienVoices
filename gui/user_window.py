from PyQt6.QtWidgets import (QMainWindow, QTabWidget, QWidget,
    QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox)
from gui.profile_page import ProfilePage
from gui.analytics_page import AnalyticsPage


class UserWindow(QMainWindow):
    def __init__(self, session, user):
        super().__init__()
        self.session = session
        self.user = user
        self.setWindowTitle("Классификатор сигналов")
        self.setMinimumSize(900, 650)
        self._build_ui()

    def _build_ui(self):
        tabs = QTabWidget()

        tabs.addTab(ProfilePage(self.user), "Профиль")
        tabs.addTab(self._build_upload_tab(), "Загрузка теста")

        self.analytics_tab = AnalyticsPage(self.session)
        tabs.addTab(self.analytics_tab, "Аналитика")

        self.setCentralWidget(tabs)

    def _build_upload_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)

        layout.addWidget(QLabel("Загрузите тестовый датасет (.npz):"))

        btn_upload = QPushButton("Выбрать файл и загрузить")
        btn_upload.clicked.connect(self._upload_file)
        layout.addWidget(btn_upload)

        self.result_label = QLabel("")
        layout.addWidget(self.result_label)

        widget.setLayout(layout)
        return widget

    def _upload_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Выберите .npz файл", "", "NPZ files (*.npz)")
        if not path:
            return
        with open(path, 'rb') as f:
            files = {'file': (path, f, 'application/octet-stream')}
            resp = self.session.post('http://localhost:5000/api/upload_test', files=files)
        if resp.status_code == 200:
            data = resp.json()
            self.result_label.setText(
                f"Файл загружен\n"
                f"Точность (Accuracy): {data['accuracy']:.4f}\n"
                f"Потери (Loss): {data['loss']:.4f}\n"
                f"Записей: {data['num_records']}"
            )
            self.analytics_tab.refresh()
        else:
            QMessageBox.warning(self, "Ошибка", resp.json().get('error', 'Ошибка загрузки'))
