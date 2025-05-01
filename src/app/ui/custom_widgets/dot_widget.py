from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt, QTimer
from ...pc_info import SystemInfo


class DotProgress(QWidget):
    def __init__(self, progress: str, parent=None):
        super().__init__(parent)
        self._progress = int(progress)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.updateProgress)
        self._timer.start(100)

    def updateProgress(self):
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        size = min(rect.width(), rect.height())
        center = rect.center()

        max_radius = int(size / 2 * 0.8)
        radius = int(max_radius * (self._progress / 100))

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#CCCCCC"))
        painter.drawEllipse(center, max_radius, max_radius)

        painter.setBrush(QColor("#4CAF50"))
        painter.drawEllipse(center, radius, radius)
