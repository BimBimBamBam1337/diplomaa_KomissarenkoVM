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

    def __init__(self, wallpaper_name):
        """
        Инициализация класса DesktopInfo.

        :param wallpaper_name: Название файла обоев.
        """
        self.system = SystemInfo()
        self.wallpaper = os.path.join(os.getcwd(), "wallpapers", wallpaper_name)

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
        Получает текущие обои рабочего стола для Linux.

        :return: Путь к текущим обоям.
        """
        command = "gsettings get org.gnome.desktop.background picture-uri"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip()

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
