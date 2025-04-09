import platform
import psutil

from datetime import datetime
from typing import Dict, Any
from pathlib import Path


class SystemInfo:

    def __init__(self):
        self.os_type = self.get_platform_info().get("system")
        self.cpu_architecture = self.get_platform_info().get("machine")
        self.uptime = self.boot_time_start().get("uptime")
        self.home_path = Path.home()

    @staticmethod
    def get_size(bytes: int = 0, sufix: str = "b") -> str:
        """
        Возвращает строковое представление размера в удобном формате (например, K, M, G).

        Аргументы:
            bytes (int): Размер в байтах.
            sufix (str): Суффикс (по умолчанию "b" для байт).

        Возвращаемое значение:
            str: Размер в удобном формате с указанным суффиксом.
        """
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes: .2f} {unit}{sufix}"
            bytes /= factor

    def get_platform_info(self) -> Dict[str, str]:
        """
        Возвращает информацию о платформе системы.

        Возвращаемое значение:
            dict: Словарь с информацией о системе, содержащий:
                - "system" (str): Операционная система.
                - "node" (str): Имя машины.
                - "release" (str): Релиз операционной системы.
                - "version" (str): Версия операционной системы.
                - "machine" (str): Тип машины.
                - "processor" (str): Процессор.
        """
        uname = platform.uname()
        return {
            "system": uname.system,
            "node": uname.node,
            "release": uname.release,
            "version": uname.version,
            "machine": uname.machine,
            "processor": uname.processor,
        }

    @staticmethod
    def boot_time_start() -> Dict[Any, Any]:
        """
        Получает информацию о времени загрузки системы и времени работы.

        Возвращаемое значение:
            dict: Словарь с ключами "boot_date", "boot_time" и "uptime", где:
                - "boot_date" (str): Дата загрузки системы.
                - "boot_time" (str): Время загрузки системы.
                - "uptime" (dict): Словарь с продолжительностью работы системы, содержащий:
                    - "days" (int): Количество дней.
                    - "hours" (int): Количество часов.
                    - "minutes" (int): Количество минут.
        """
        boot_time_timestamp = psutil.boot_time()
        boot_time = datetime.fromtimestamp(boot_time_timestamp)
        now = datetime.now()
        uptime = now - boot_time

        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        return {
            "boot_date": boot_time.strftime("%d.%m.%Y"),
            "boot_time": boot_time.strftime("%H:%M:%S"),
            "uptime": {
                "days": days,
                "hours": hours,
                "minutes": minutes,
            },
        }

    @staticmethod
    def get_vmem() -> Dict[str, str]:
        """
        Получает информацию о виртуальной памяти системы.

        Возвращаемое значение:
            dict: Словарь с информацией о памяти системы, содержащий:
                - "total" (str): Общий объём памяти.
                - "available" (str): Доступная память.
                - "percent" (str): Процент использования памяти.
                - "used" (str): Используемая память.
                - "free" (str): Свободная память.
                - "active" (str): Активная память.
                - "inactive" (str): Неактивная память.
                - "buffers" (str): Буферы.
                - "cached" (str): Кэш.
                - "shared" (str): Общая память.
                - "slab" (str): Память в слэбах.
        """
        svmem = psutil.virtual_memory()
        return {
            "total": SystemInfo.get_size(svmem.total),
            "available": SystemInfo.get_size(svmem.available),
            "percent": f"{svmem.percent}%",
            "used": SystemInfo.get_size(svmem.used),
            "free": SystemInfo.get_size(svmem.free),
            "active": SystemInfo.get_size(svmem.active),
            "inactive": SystemInfo.get_size(svmem.inactive),
            "buffers": SystemInfo.get_size(svmem.buffers),
            "cached": SystemInfo.get_size(svmem.cached),
            "shared": SystemInfo.get_size(svmem.shared),
            "slab": SystemInfo.get_size(svmem.slab),
        }

    def get_disk_usage(self) -> Dict:
        """
        Получает информацию об использовании диска.

        Возвращаемое значение:
            dict: Словарь с информацией о дисках и их использовании:
                - Каждый ключ словаря — это путь к устройству (например, "/dev/sda1"),
                  а значение — словарь, содержащий:
                    - "mountpoint" (str): Точка монтирования.
                    - "fstype" (str): Тип файловой системы.
                    - "total" (str): Общий размер.
                    - "used" (str): Используемый размер.
                    - "free" (str): Свободный размер.
                    - "percent_used" (str): Процент использования.
        """
        partitions = psutil.disk_partitions()
        disk_info = {}

        for partition in partitions:
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except Exception:
                continue

            disk_info[partition.device] = {
                "mountpoint": partition.mountpoint,
                "fstype": partition.fstype,
                "total": self.get_size(partition_usage.total).strip(),
                "used": self.get_size(partition_usage.used).strip(),
                "free": self.get_size(partition_usage.free).strip(),
                "percent_used": f"{partition_usage.percent}%",
            }

        return disk_info
