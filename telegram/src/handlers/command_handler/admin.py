from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

from src.filters import IsAdmin

router = Router()


@router.message(Command("admin"), IsAdmin())
async def admin_handler(message: Message):
    await message.answer(
        text=r"""🛠️ *Административные команды* 🛠️

*Управление пользователями:*
▫️ `/list_engineers` \- Список всех инженеров
▫️ `/list_professors` \- Список всех преподавателей
▫️ `/find_user <id/username>` \- Поиск пользователя

 `/reassign <task_id> <engineer_id>` \- Переназначить задачу

*Системные команды:*
▫️ `/broadcast <text>` \- Рассылка сообщения
▫️ `/logs` \- Получить логи системы
""",
        parse_mode=ParseMode.MARKDOWN_V2,
    )
