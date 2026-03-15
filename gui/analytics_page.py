"""
Страница с 4 графиками. Использует matplotlib встроенный в PyQt6.
Все графики масштабируемы (zoom/pan через toolbar matplotlib).
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavToolbar
from matplotlib.figure import Figure
import numpy as np


def make_chart_widget(parent, fig):
    """Оборачивает Figure в виджет с тулбаром (zoom, pan)"""
    widget = QWidget(parent)
    layout = QVBoxLayout()
    canvas = FigureCanvas(fig)
    toolbar = NavToolbar(canvas, widget)
    layout.addWidget(toolbar)
    layout.addWidget(canvas)
    widget.setLayout(layout)
    return widget, canvas


class AnalyticsPage(QWidget):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.tabs = QTabWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)
        self.refresh()

    def refresh(self):
        self.tabs.clear()
        self._add_training_chart()
        self._add_distribution_chart()
        self._add_valid_top5_chart()
        self._add_confidence_chart()

    def _add_training_chart(self):
        resp = self.session.get('http://localhost:5000/api/analytics/training')
        if resp.status_code != 200:
            return
        h = resp.json()

        fig = Figure(figsize=(8, 4))
        ax = fig.add_subplot(111)
        ax.plot(h.get('accuracy', []), label='Train accuracy')
        ax.plot(h.get('val_accuracy', []), label='Val accuracy')
        ax.set_xlabel('Эпоха')
        ax.set_ylabel('Точность')
        ax.set_title('Точность по эпохам обучения')
        ax.legend()
        ax.grid(True)

        w, _ = make_chart_widget(self, fig)
        self.tabs.addTab(w, "Обучение")

    def _add_distribution_chart(self):
        resp = self.session.get('http://localhost:5000/api/analytics/train_distribution')
        if resp.status_code != 200:
            return
        data = resp.json()

        fig = Figure(figsize=(10, 4))
        ax = fig.add_subplot(111)
        ax.bar([str(l) for l in data['labels']], data['counts'])
        ax.set_xlabel('Класс (цивилизация)')
        ax.set_ylabel('Количество записей')
        ax.set_title('Распределение классов в обучающем наборе')
        fig.tight_layout()

        w, _ = make_chart_widget(self, fig)
        self.tabs.addTab(w, "Классы (train)")

    def _add_valid_top5_chart(self):
        resp = self.session.get('http://localhost:5000/api/analytics/valid_top5')
        if resp.status_code != 200:
            return
        data = resp.json()

        fig = Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        ax.barh([f"Класс {l}" for l in data['labels']], data['counts'], color='coral')
        ax.set_xlabel('Количество записей')
        ax.set_title('Топ-5 классов в валидационном наборе')
        fig.tight_layout()

        w, _ = make_chart_widget(self, fig)
        self.tabs.addTab(w, "Топ-5 (valid)")

    def _add_confidence_chart(self):
        resp = self.session.get('http://localhost:5000/api/analytics/test_confidence')
        if resp.status_code != 200:
            return
        data = resp.json()

        confidence = data['confidence']
        correct = data['correct']

        fig = Figure(figsize=(10, 4))
        ax = fig.add_subplot(111)
        colors = ['green' if c else 'red' for c in correct]
        ax.bar(range(len(confidence)), confidence, color=colors, width=1.0)
        ax.set_xlabel('Номер записи')
        ax.set_ylabel('Уверенность модели')
        ax.set_title('Точность определения каждой записи (зелёный = верно, красный = ошибка)')
        ax.set_ylim(0, 1)
        fig.tight_layout()

        w, _ = make_chart_widget(self, fig)
        self.tabs.addTab(w, "Тест (детально)")
