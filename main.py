import sys

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Qt signals & Slots")
        self.setGeometry(100, 100, 320, 210)
        label = QLabel()
        pixmap = QPixmap("sevsu.jpg")
        label.setPixmap(pixmap)
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    sys.exit(app.exec())
