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
        self.node = self.get_platform_info().get("node")
        self.home_path = Path.home()

    @staticmethod
    def get_size(bytes: int = 0, sufix: str = "b") -> str:
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes: .2f} {unit}{sufix}"
            bytes /= factor

    def get_platform_info(self) -> Dict[str, str]:
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
    def get_vmem() -> Dict[str, any]:
        svmem = psutil.virtual_memory()
        return {
            "total": SystemInfo.get_size(svmem.total),
            "available": SystemInfo.get_size(svmem.available),
            "percent_used": svmem.percent,
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
                "percent_used": {partition_usage.percent},
            }

        return disk_info
