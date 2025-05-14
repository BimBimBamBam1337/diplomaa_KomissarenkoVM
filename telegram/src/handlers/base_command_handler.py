from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        text="""🔧 <b>Добро пожаловать в бот технической поддержки!</b> 🔧

Здесь вы можете:
✅ Создавать задачи для инженеров
✅ Отслеживать статус выполнения
✅ Общаться со специалистами
✅ Управлять своими запросами

✨ <b>Как это работает?</b> ✨

1. 🆕 <b>Создать задачу</b>
→ Нажмите /new_task
→ Опишите проблему
→ Укажите срочность (🚨 критическая/⚠️ средняя/🕒 низкая)

2. 🕵️ <b>Отслеживать статус</b>
→ Текущие задачи: /my_tasks
→ История выполненных: /history
→ Уведомления при изменении статуса

3. ✉️ <b>Связь с инженером</b>
→ Возможность прикреплять скриншоты
→ Уведомления о ответах (🔔)

🔨 <b>Дополнительные возможности</b>
→ Редактировать задачу: /edit_task
→ Отменить запрос: /cancel_task
→ Срочный вызов инженера: /sos
→ Просмотреть задачу по ID: /find_task
→ Просмотреть задачи на сегодня: /tasks_today
""",
        parse_mode=ParseMode.HTML,
    )
