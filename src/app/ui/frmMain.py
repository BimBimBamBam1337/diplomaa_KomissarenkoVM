from PyQt6.QtGui import QGuiApplication, QPixmap
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QLabel, QMainWindow

from ..pc_info import SystemInfo
from .custom_widgets import DotProgress
from ..config import ASSETS


class TestWidget:
    def setupUi(self, frmMain: QMainWindow):
        screen = QGuiApplication.primaryScreen()
        available_geometry = screen.availableGeometry()

        label = QLabel()

        pixmap_computer = QPixmap(ASSETS + "computer.png")

        label.setPixmap(pixmap_computer)

        window_width = 600
        window_height = 400

        sys_info = SystemInfo()
        vmem = sys_info.get_vmem()
        progress_value = vmem.get("percent", 0)

        self.dot_widget = DotProgress(progress=progress_value, parent=self)
        self.dot_widget1 = DotProgress(progress=progress_value, parent=self)

        self.dot_widget.move(30, 30)
        self.dot_widget.move(200, 200)
        x = int(
            (available_geometry.width() - window_width) / 2 + available_geometry.x()
        )
        y = int(
            (available_geometry.height() - window_height) / 2 + available_geometry.y()
        )

        frmMain.setCentralWidget(label)
        frmMain.resize(pixmap_computer.width(), pixmap_computer.height())
        frmMain.setWindowTitle("Application")
        frmMain.setGeometry(x, y, window_width, window_height)
        QtCore.QMetaObject.connectSlotsByName(frmMain)

    # def retranslateUi(self, frmMain):
    #     _translate = QtCore.QCoreApplication.translate
    #     frmMain.setWindowTitle(_translate("frmMain", "MainWindow"))
    #     self.btnTryMe.setText(_translate("frmMain", "Try Me"))
