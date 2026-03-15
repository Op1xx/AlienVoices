import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QLabel, QFileDialog, QMessageBox,
)
from PyQt6.QtCore import Qt
from app.ml.preprocessor import extract_features
from app.ml.model import load_model, predict
from app.database.models import get_connection


CLASS_NAMES = {
    0: "Зета Ретикули",
    1: "Серые",
    2: "Плеядеанцы",
    3: "Рептилоиды",
    4: "Нордики",
}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AlienVoices — Классификатор голосов")
        self.setMinimumSize(480, 320)

        self._model = None

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.label_file = QLabel("Файл не выбран")
        self.label_file.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_result = QLabel("")
        self.label_result.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_open = QPushButton("Открыть аудиофайл")
        btn_open.clicked.connect(self._open_file)

        btn_classify = QPushButton("Классифицировать")
        btn_classify.clicked.connect(self._classify)

        layout.addWidget(self.label_file)
        layout.addWidget(btn_open)
        layout.addWidget(btn_classify)
        layout.addWidget(self.label_result)

        self._current_file = None

    def _open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Выбрать аудиофайл", "", "Audio (*.wav *.mp3 *.flac)"
        )
        if path:
            self._current_file = path
            self.label_file.setText(path)

    def _classify(self):
        if not self._current_file:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите файл")
            return
        try:
            if self._model is None:
                self._model = load_model()
            features = extract_features(self._current_file)
            class_id, confidence = predict(self._model, features)
            name = CLASS_NAMES.get(class_id, f"Класс {class_id}")
            self.label_result.setText(f"{name}  ({confidence:.1%})")

            with get_connection() as conn:
                import os
                conn.execute(
                    "INSERT INTO voice_samples (filename, alien_class, confidence) VALUES (?, ?, ?)",
                    (os.path.basename(self._current_file), str(class_id), confidence),
                )
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))


def run_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
