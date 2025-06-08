from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import (
    QTimer,
    Qt,
    QPropertyAnimation,
    QEasingCurve,
    pyqtProperty,
    pyqtSignal,
)
from PyQt6.QtGui import QPainter, QColor, QBrush, QMouseEvent


class DotProgress(QWidget):
    clicked = pyqtSignal()  # 💥 Новый сигнал

    def __init__(
        self,
        progress: int | float = 0,
        parent=None,
        is_correct_wallpaper: bool | None = None,
        label: str = "Значение",
    ):
        super().__init__(parent)
        self.setFixedSize(30, 30)

        self._progress = 0
        self._target_progress = max(0, min(100, progress))
        self._is_correct_wallpaper = is_correct_wallpaper
        self._label = label

        self.outer_color = QColor("#CCCCCC")
        self.low_color = QColor("#4CAF50")
        self.medium_color = QColor("#FFC107")
        self.high_color = QColor("#F44336")

        self.animation = QPropertyAnimation(self, b"progress")
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.Type.OutQuad)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self.update)
        self._timer.start(30)

        self.set_progress(self._target_progress, animate=True)

    @pyqtProperty(int)
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        self._progress = max(0, min(100, value))
        self.update_tooltip()
        self.update()

    def update_tooltip(self):
        if self._is_correct_wallpaper is not None:
            state = "правильные" if self._is_correct_wallpaper else "неправильные"
            tooltip = f"{self._label}: {state}"
        else:
            tooltip = f"{self._label}: {self._progress}%"
        self.setToolTip(tooltip)

    def get_progress_color(self):
        if self._is_correct_wallpaper is True:
            return self.low_color
        elif self._is_correct_wallpaper is False:
            return self.high_color
        else:
            if self._progress < 50:
                return self.low_color
            elif 50 <= self._progress < 75:
                return self.medium_color
            else:
                return self.high_color

    def set_progress(self, value: int, animate: bool = True):
        self._target_progress = max(0, min(100, value))

        if animate:
            self.animation.stop()
            self.animation.setStartValue(self._progress)
            self.animation.setEndValue(self._target_progress)
            self.animation.start()
        else:
            self.progress = self._target_progress

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        size = min(rect.width(), rect.height())
        center = rect.center()

        max_radius = int(size / 2 * 0.8)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(self.outer_color))
        painter.setBrush(QBrush(self.get_progress_color()))
        painter.drawEllipse(center, max_radius, max_radius)

    def set_threshold_colors(self, low: str, medium: str, high: str):
        self.low_color = QColor(low)
        self.medium_color = QColor(medium)
        self.high_color = QColor(high)
        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()  # 🔔 Клик!
        super().mousePressEvent(event)
