import os
from typing import Dict
import pyautogui
import ctypes
import subprocess
from .sys_info import SystemInfo


class DesktopInfo:
    """
    Класс для получения информации о рабочем столе и обоях пользователя.
    """

    def __init__(self, wallpaper: str):
        """
        Инициализация класса DesktopInfo.

        """
        self.wallpaper = wallpaper
        self.system = SystemInfo()

    def get_desktop_info(self) -> Dict:
        """
        Получает информацию о разрешении экрана и пути к рабочему столу.

        :return: Словарь с разрешением экрана и путем к рабочему столу.
        """
        screen_width, screen_height = pyautogui.size()
        desktop_path = self.system.home_path / "Desktop"
        return {
            "screen_width": screen_width,
            "screen_height": screen_height,
            "path": f"{desktop_path}",
        }

    def get_desktop_files(self):
        """
        Получает количество файлов на рабочем столе.

        :return: Количество файлов на рабочем столе.
        """
        files = os.listdir(self.get_desktop_info().get("path"))
        return len(files)

    def get_wallpaper(self):
        """
        Получает текущие обои рабочего стола в зависимости от ОС.

        :return: Путь к текущим обоям.
        """
        return (
            self._get_wallpaper_windows()
            if self.system.os_type == "Windows"
            else self._get_wallpaper_linux()
        )

    def _get_wallpaper_linux(self):
        """
        Получает имя файла текущих обоев рабочего стола для Linux (GNOME).

        :return: Имя файла обоев (например, 'image.jpg') или None, если ошибка.
        """
        try:
            command = "gsettings get org.gnome.desktop.background picture-uri"
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, check=True
            )

            # Очищаем вывод: убираем кавычки и 'file://'
            wallpaper_uri = result.stdout.strip().strip("'")
            wallpaper_path = wallpaper_uri.replace("file://", "")
            file_name = os.path.basename(wallpaper_path)
            if file_name == self.wallpaper:
                return True
            return False

        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Ошибка при получении обоев: {e}")
            return None

    def _get_wallpaper_windows(self):
        """
        Получает текущие обои рабочего стола для Windows.

        :return: Путь к текущим обоям.
        """
        SPI_GETDESKWALLPAPER = 20
        MAX_PATH = 260
        buffer = ctypes.create_unicode_buffer(MAX_PATH)
        ctypes.windll.user32.SystemParametersInfoW(
            SPI_GETDESKWALLPAPER, MAX_PATH, buffer, 0
        )
        return buffer.value
