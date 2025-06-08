from datetime import datetime
from typing import Type

from src.postgres.models import Base


def format_date(dt: datetime | None) -> str:
    return dt.strftime("%d.%m.%Y %H:%M") if dt else "не указано"


def get_task_response(task):
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


def get_entity_respone(entity: Base):
    return f"""
ID: {entity.id}
ФИО: {entity.first_name} {entity.midle_name} {entity.last_name}
Имя пользователя: @{entity.username}
    """
