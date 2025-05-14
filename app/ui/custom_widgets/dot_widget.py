from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer, Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QPainter, QColor, QBrush


class DotProgress(QWidget):
    def __init__(
        self, progress: int | float = 0, parent=None, is_correct_wallpaper: bool = True
    ):
        super().__init__(parent)
        self.setFixedSize(30, 30)

        self._progress = 0
        self._target_progress = max(0, min(100, progress))
        self._is_correct_wallpaper = is_correct_wallpaper

        # Цвета для разных уровней загруженности
        self.outer_color = QColor("#CCCCCC")
        self.low_color = QColor("#4CAF50")  # Зелёный (<50%)
        self.medium_color = QColor("#FFC107")  # Жёлтый (50-75%)
        self.high_color = QColor("#F44336")  # Красный (>75%)

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
        self.update()

    # def get_progress_color(self):
    #     """Возвращает цвет в зависимости от уровня загруженности"""
    #     if self._progress < 50:
    #         return self.low_color
    #     elif 50 <= self._progress < 75:
    #         return self.medium_color
    #     else:
    #         return self.high_color

    def get_progress_color(self):
        """Цвет:
        - зелёный, если is_correct_wallpaper=True,
        - красный, если is_correct_wallpaper=False,
        - по прогрессу, если is_correct_wallpaper=None.
        """
        if self._is_correct_wallpaper is True:
            return self.low_color
        elif self._is_correct_wallpaper is False:
            return self.high_color
        else:  # None → цвет зависит от прогресса
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

        # Внешний круг (фон)
        max_radius = int(size / 2 * 0.8)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(self.outer_color))
        painter.setBrush(QBrush(self.get_progress_color()))
        painter.drawEllipse(center, max_radius, max_radius)

    def set_threshold_colors(self, low: str, medium: str, high: str):
        """Устанавливает пороговые цвета"""
        self.low_color = QColor(low)
        self.medium_color = QColor(medium)
        self.high_color = QColor(high)
        self.update()
