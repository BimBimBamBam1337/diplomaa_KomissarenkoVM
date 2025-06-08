import socket
import json
import time
import threading
from sys_info import SystemInfo

SERVER_HOST = "192.168.0.176"
SERVER_DATA_PORT = 9000
CLIENT_FILE_PORT = 9001  # другой порт для получения файла


def collect_data():
    sys_info = SystemInfo()
    disks = sys_info.get_disk_usage()

    # Усреднённый процент занятого места на дисках
    try:
        percent_list = [next(iter(d.get("percent_used", {0}))) for d in disks.values()]
        avg = round(sum(percent_list) / len(percent_list), 2)
    except Exception:
        avg = 0.0

    return {
        "client_id": f"{sys_info.node}:{sys_info.os_type}:{sys_info.cpu_architecture}",
        "ip": get_local_ip(),  # передаём IP явно
        "percent_used": sys_info.get_vmem().get("percent_used", 0),
        "disks_avg": avg,
        "wallpaper": False,
        "uptime": f"{sys_info.uptime.get('days')}d {sys_info.uptime.get('hours')}h {sys_info.uptime.get('minutes')}m",
    }


def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"


def start_file_listener(host="0.0.0.0", port=CLIENT_FILE_PORT):
    def _listen():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            s.listen()
            print(f"[CLIENT] Listening for file on {host}:{port}")
            while True:
                conn, _ = s.accept()
                with conn:
                    filename = conn.recv(1024).decode().strip()
                    with open(filename, "wb") as f:
                        while True:
                            data = conn.recv(4096)
                            if not data:
                                break
                            f.write(data)
                    print(f"[CLIENT] Получен файл: {filename}")

    threading.Thread(target=_listen, daemon=True).start()


def send_to_server(host=SERVER_HOST, port=SERVER_DATA_PORT):
    data = collect_data()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((host, port))
            s.send(json.dumps(data).encode("utf-8"))
    except (ConnectionRefusedError, socket.timeout) as e:
        print(f"[!] Не удалось подключиться к серверу: {e}")
    except Exception as e:
        print(f"[!] Ошибка при отправке данных: {e}")


if __name__ == "__main__":
    start_file_listener()
    time.sleep(1)  # Подождать, пока сокет начнёт слушать
    while True:
        send_to_server()
        time.sleep(10)
