import sys
import ui.frmMain as main_form
from PyQt6.QtWidgets import QMainWindow, QApplication, QVBoxLayout


class MyAppName(QMainWindow, main_form.TestWidget):
    def __init__(self, parent=None):
        super(MyAppName, self).__init__(parent)
        self.setupUi(self)

        self.show()


def refresh():
    QApplication.processEvents()


def main():
    app = QApplication(sys.argv)
    form = MyAppName()
    form.show()
    app.exec()


if __name__ == "__main__":
    main()
