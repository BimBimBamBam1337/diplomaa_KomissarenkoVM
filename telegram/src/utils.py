import re

from datetime import datetime
from .mongo import Task


def escape_md(text: str) -> str:
    return re.sub(r"([_*\[\]()~`>#+\-=|{}.!\\])", r"\\\1", str(text))


def format_date(dt: datetime | None) -> str:
    return dt.strftime("%d.%m.%Y %H:%M") if dt else "не указано"


def get_task_response(task: Task):
    return (
        f"📌 *{task.get('task_name')}* \n"
        f"`ID: {task.get('task_id')}`\n\n"
        f"*Описание:*\n{task.get('description')}\n\n"
        f"👨🏫 *Преподаватель:* `{task.get('professor_id')}`\n"
        f"👨🔧 *Исполнитель:* `{task.get('engineer_id') or 'не назначен'}`\n\n"
        f"📅 *Создана:* `{format_date(task.get('created_at'))}`\n"
        f"⏱ *Начата:* `{format_date(task.get('started_at'))}`\n"
        f"🏁 *Завершена:* `{format_date(task.get('completed_at'))}`\n"
        f"⏰ *Дедлайн:* `{task.get('deadline') or 'не установлен'}`"
    )
