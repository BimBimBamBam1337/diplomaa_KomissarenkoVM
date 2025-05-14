import os
import sys

from loguru import logger

os.makedirs("logs", exist_ok=True)

logger.remove()

logger.add(
    "logs/bot.log", level="INFO", rotation="1 MB", retention="7 days"
)  # Логи в файл
logger.add(sys.stdout, level="INFO")  # Логи в консоль

logger.add(
    "logs/errors.log", level="ERROR", rotation="1 MB", retention="7 days"
)  # Логи ошибок в файл
logger.add(sys.stdout, level="ERROR")  # Логи ошибок в консоль
