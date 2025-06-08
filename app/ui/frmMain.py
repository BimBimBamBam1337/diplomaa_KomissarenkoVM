from PyQt6.QtGui import QGuiApplication, QPixmap
from PyQt6 import QtCore
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
    QPushButton,
    QLineEdit,
    QDialog,
)
from PyQt6.QtCore import Qt

from .server import Server
from pc_info import SystemInfo, DesktopInfo
from .custom_widgets import DotProgress
from config import ASSETS


class AdminWidget:
    def setupUi(self, frmMain: QMainWindow):
        screen = QGuiApplication.primaryScreen()
        server = Server()
        available_geometry = screen.availableGeometry()
        window_width = 900
        window_height = 500

        vmem_load = self._get_vmem_load()
        disks_load = self._get_disks_load()
        di = DesktopInfo("sevsu.jpg")
        is_correct_wallpaper = di.get_wallpaper()

        central_widget = QWidget()
        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.setContentsMargins(30, 20, 30, 20)
        self.main_layout.setSpacing(30)

        # Админский комп
        self.admin_wrapper = self.setup_wrapper()
        self.main_pixmap = self.setup_computer_pixmap()
        self.main_progress_container = self.setup_progress_container()

        self.vmem_dot_widget = DotProgress(progress=vmem_load, parent=self, label="ОЗУ")
        self.disks_dot_widget = DotProgress(
            progress=disks_load, parent=self, label="Диски"
        )
        self.wallpaper_dot = DotProgress(
            is_correct_wallpaper=is_correct_wallpaper, parent=self, label="Обои"
        )
        self.wallpaper_dot.clicked.connect(di.set_wallpaper_gnome)

        self.main_progress_container.layout().addWidget(self.vmem_dot_widget)
        self.main_progress_container.layout().addWidget(self.disks_dot_widget)
        self.main_progress_container.layout().addWidget(self.wallpaper_dot)

        self.admin_wrapper.layout().addWidget(self.main_pixmap)
        self.admin_wrapper.layout().addWidget(self.main_progress_container)

        left_panel = QWidget()
        left_panel.setFixedWidth(250)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        left_layout.addWidget(self.admin_wrapper)

        self.main_layout.addWidget(left_panel)

        # Клиенты
        self.clients_widget = QWidget()
        self.clients_container = QVBoxLayout(self.clients_widget)
        self.clients_container.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.clients_container.setSpacing(10)

        self.clients_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )

        self.main_layout.addWidget(self.clients_widget)

        # Окно
        x = int(
            (available_geometry.width() - window_width) / 2 + available_geometry.x()
        )
        y = int(
            (available_geometry.height() - window_height) / 2 + available_geometry.y()
        )

        frmMain.setCentralWidget(central_widget)
        frmMain.setGeometry(x, y, window_width, window_height)
        frmMain.setWindowTitle("Мониторинг")
        QtCore.QMetaObject.connectSlotsByName(frmMain)

    def _get_vmem_load(self) -> int:
        return SystemInfo().get_vmem().get("percent_used", 0)

    def _get_disks_load(self) -> float:
        disks_info = [
            next(iter(_.get("percent_used", {0})))
            for _ in SystemInfo().get_disk_usage().values()
        ]
        return round(sum(disks_info) / len(disks_info), 2)

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

    def add_client_info_widget(self, client_id: str, data: dict):
        for i in range(self.clients_container.count()):
            widget = self.clients_container.itemAt(i).widget()
            if widget and widget.objectName() == client_id:
                layout = widget.layout()
                row_layout = layout.itemAt(1).layout()

                dot_layout = row_layout.itemAt(0).layout()

                mem = dot_layout.itemAt(0).widget()
                disk = dot_layout.itemAt(1).widget()
                wall = dot_layout.itemAt(2).widget()

                mem.set_progress(data.get("percent_used", 0))
                disk.set_progress(data.get("disks_avg", 0))

                uptime_label = layout.itemAt(2).widget()
                uptime_label.setText(f"Uptime: {data.get('uptime', '???')}")
                return

        # Новый виджет
        widget = QWidget()
        widget.setObjectName(client_id)
        widget.setStyleSheet(
            "background-color: #f0f0f0; border: 1px solid #ccc; border-radius: 10px;"
        )
        widget.setMinimumHeight(100)

        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel(f"{client_id}")
        title.setStyleSheet("font-weight: bold;")

        # Кнопка справа
        button = QPushButton("🛈")
        button.setFixedSize(30, 30)
        button.setStyleSheet("border-radius: 15px; font-weight: bold;")
        button.clicked.connect(lambda _, cid=client_id: self.show_input_dialog(cid))

        # Dot-индикаторы слева
        mem = DotProgress(progress=data.get("percent_used", 0), label="ОЗУ")
        disk = DotProgress(progress=data.get("disks_avg", 0), label="Диски")
        wall = DotProgress(
            is_correct_wallpaper=data.get("wallpaper", False), label="Обои"
        )

        dot_layout = QHBoxLayout()
        dot_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        dot_layout.addWidget(mem)
        dot_layout.addWidget(disk)
        dot_layout.addWidget(wall)

        # Горизонтальный слой: слева dot-прогрессы, справа кнопка
        row_layout = QHBoxLayout()
        row_layout.addLayout(dot_layout)
        row_layout.addStretch()  # Чтобы занять всё пространство между
        row_layout.addWidget(button)

        uptime_label = QLabel(f"Uptime: {data.get('uptime', '???')}")
        uptime_label.setStyleSheet("font-size: 10pt; color: #666;")

        layout.addWidget(title)
        layout.addLayout(row_layout)
        layout.addWidget(uptime_label)

        self.clients_container.addWidget(widget)
        self.clients_widget.update()

    def process_dialog_input(self, client_id, text, dialog):
        print(f"[{client_id}] Введён текст: {text}")
        dialog.accept()  # Закрыть окно

        # Отправка файла клиенту
        self.server.send_file_to_client(client_id, text)

    def show_input_dialog(self, client_id):
        dialog = QDialog(self)
        dialog.setWindowTitle("Введите имя файла")

        layout = QVBoxLayout(dialog)
        input_field = QLineEdit()
        send_button = QPushButton("Отправить")

        layout.addWidget(input_field)
        layout.addWidget(send_button)

        # При нажатии на кнопку — передать содержимое поля
        send_button.clicked.connect(
            lambda: self.process_dialog_input(client_id, input_field.text(), dialog)
        )

        dialog.exec()
