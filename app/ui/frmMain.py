from PyQt6.QtGui import QGuiApplication, QPixmap
from PyQt6 import QtCore
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtCore import Qt


from ..pc_info import SystemInfo, DesktopInfo
from .custom_widgets import DotProgress
from ..config import ASSETS, WALLPAPERS


class TestWidget:
    def setupUi(self, frmMain: QMainWindow):
        screen = QGuiApplication.primaryScreen()
        available_geometry = screen.availableGeometry()
        window_width = 900
        window_height = 500
        vmem_load = self._get_vmem_load()
        disks_load = self._get_disks_load()
        is_correct_wallpaper = DesktopInfo("sevsu.jpg").get_wallpaper()

        # Центральный контейнер (нужен для QMainWindow)
        central_widget = QWidget()
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignHCenter
        )
        self.main_layout.setContentsMargins(70, 0, 0, 0)
        self.main_layout.setSpacing(10)

        # Обёртка с вертикальным лэйаутом
        self.main_wrapper = self.setup_wrapper()

        # Виджет с изображением
        self.main_pixmap = self.setup_computer_pixmap()

        # Контейнер под кастомные прогресс-боллы
        self.main_progress_container = self.setup_progress_container()

        # Инициализация кастомных DotProgress
        self.vmem_dot_widget = DotProgress(
            progress=vmem_load,
            parent=self,
        )
        self.disks_dot_widget = DotProgress(progress=disks_load, parent=self)
        self.wallpaper_dot = DotProgress(
            parent=self, is_correct_wallpaper=is_correct_wallpaper
        )
        # Расположение
        self.main_progress_container.layout().addWidget(self.vmem_dot_widget)
        self.main_progress_container.layout().addWidget(self.disks_dot_widget)
        self.main_progress_container.layout().addWidget(self.wallpaper_dot)
        self.main_wrapper.layout().addWidget(self.main_pixmap)
        self.main_wrapper.layout().addWidget(self.main_progress_container)
        self.main_layout.addWidget(self.main_wrapper)

        # Настройка главного окна
        x = int(
            (available_geometry.width() - window_width) / 2 + available_geometry.x()
        )
        y = int(
            (available_geometry.height() - window_height) / 2 + available_geometry.y()
        )

        frmMain.setCentralWidget(central_widget)
        frmMain.setGeometry(x, y, window_width, window_height)
        frmMain.setWindowTitle("Application")
        QtCore.QMetaObject.connectSlotsByName(frmMain)

    def _get_vmem_load(self) -> int:
        return SystemInfo().get_vmem().get("percent_used", 0)

    def _get_disks_load(self) -> float:
        disks_info = [
            next(iter(_.get("percent_used", {0})))
            for _ in SystemInfo().get_disk_usage().values()
        ]
        disks_load = round(sum(disks_info) / len(disks_info), 2)
        return disks_load

    def setup_wrapper(self):
        wrapper = QWidget()
        wrapper.setFixedSize(200, 200)

        wrapper_layout = QVBoxLayout(wrapper)
        wrapper_layout.setSpacing(10)
        wrapper_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )
        return wrapper

    def setup_computer_pixmap(self) -> QLabel:
        image_label = QLabel()
        pixmap = QPixmap(ASSETS + "computer.png")
        image_label.setPixmap(pixmap)
        return image_label

    def setup_progress_container(self):
        progress_container = QWidget()
        progress_container.setFixedWidth(120)

        progress_layout = QHBoxLayout(progress_container)
        progress_layout.setContentsMargins(0, 0, 0, 0)
        progress_layout.setSpacing(10)
        progress_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        return progress_container

    # def retranslateUi(self, frmMain):
    #     _translate = QtCore.QCoreApplication.translate
    #     frmMain.setWindowTitle(_translate("frmMain", "MainWindow"))
    #     self.btnTryMe.setText(_translate("frmMain", "Try Me"))
