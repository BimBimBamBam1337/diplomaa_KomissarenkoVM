import os
import pyautogui
import ctypes
import subprocess
from .sys_info import SystemInfo


class DesktopInfo:

    def __init__(self, wallpaper_name):
        self.system = SystemInfo()
        self.wallpaper = os.path.join(os.getcwd(), "wallpapers", wallpaper_name)

    def get_desktop_info(self):
        screen_width, screen_height = pyautogui.size()
        desktop_path = self.system.home_path / "Desktop"
        return {
            "resolution": f"{screen_width}x{screen_height}",
            "path": f"{desktop_path}",
        }

    def get_desktop_files(self):
        files = os.listdir(self.get_desktop_info().get("path"))
        return len(files)

    # def set_wallpaper(self):

    def get_wallpaper(self):
        return (
            self.get_wallpaper_windows()
            if self.system.os_type == "Windows"
            else self.get_wallpaper_linux()
        )

    def get_wallpaper_linux(self):
        command = "gsettings get org.gnome.desktop.background picture-uri"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip()

    def get_wallpaper_windows(self):
        SPI_GETDESKWALLPAPER = 20
        MAX_PATH = 260
        buffer = ctypes.create_unicode_buffer(MAX_PATH)
        ctypes.windll.user32.SystemParametersInfoW(
            SPI_GETDESKWALLPAPER, MAX_PATH, buffer, 0
        )
        return buffer.value
