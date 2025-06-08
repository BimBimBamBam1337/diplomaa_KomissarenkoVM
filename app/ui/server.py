import socket
import json
import threading
import os
import time
from PyQt6.QtCore import QObject, pyqtSignal


class Server(QObject):
    data_received = pyqtSignal(str, dict)  # client_id, data

    def __init__(self, host="192.168.0.176", port=9000, parent=None):
        super().__init__(parent)
        self.host = host
        self.port = port
        self.client_ips = {}  # client_id -> IP

    def start(self):
        thread = threading.Thread(target=self._listen, daemon=True)
        thread.start()

    def _listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen()
            print(f"[+] Server listening on {self.host}:{self.port}")
            while True:
                conn, addr = s.accept()
                threading.Thread(
                    target=self._handle_client, args=(conn, addr), daemon=True
                ).start()

    def _handle_client(self, conn, addr):
        with conn:
            try:
                data = conn.recv(2048)
                if not data:
                    return

                decoded = json.loads(data.decode())

                client_id = decoded.get("client_id", "Unknown")

                # Получаем IP из payload, если есть, иначе используем addr[0]
                client_ip = decoded.get("ip", addr[0])
                self.client_ips[client_id] = client_ip

                print(f"[>] Received from {client_id} @ {client_ip}: {decoded}")

                self.data_received.emit(client_id, decoded)
            except Exception as e:
                print(f"[!] Error while handling client: {e}")

    def send_file_to_client(self, client_id, file_path, port=9001):
        client_ip = self.client_ips.get(client_id)
        if not client_ip:
            print(f"[SERVER] Нет IP-адреса для клиента {client_id}")
            return

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print(
                    f"[SERVER] Подключение к {client_ip}:{port} для отправки файла..."
                )
                s.connect((client_ip, port))

                filename = os.path.basename(file_path)
                s.send(filename.encode() + b"\n")
                time.sleep(0.5)

                with open(file_path, "rb") as f:
                    while chunk := f.read(4096):
                        s.send(chunk)

            print(f"[SERVER] Файл '{filename}' отправлен клиенту {client_ip}:{port}")
        except Exception as e:
            print(f"[SERVER] Ошибка при отправке файла: {e}")
