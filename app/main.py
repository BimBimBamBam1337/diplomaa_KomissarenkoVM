import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from ui.server import Server
from ui.frmMain import AdminWidget  # твой интерфейс с add_client_info_widget


class MyApp(QMainWindow, AdminWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.server = Server()
        self.server.data_received.connect(self.add_client_info_widget)
        self.server.start()

        self.show()


def main():
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
