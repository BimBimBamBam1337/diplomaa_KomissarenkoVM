from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

from src.filters import IsEngineer
from src.mongo import get_all_tasks, get_today_tasks, get_tasks_by_id
from src.utils import get_task_response
from src.inline_buttons import get_accept_taks_id

router = Router()


@router.message(Command("engineer"), IsEngineer())
async def engineer_handler(message: Message):
    await message.answer(
        text="🔧 <b>Инженерное меню</b>\n\n"
        "📋 /all_tasks — Все задачи\n"
        "📅 /tasks_today — Задачи на сегодня\n"
        "👤 /my_tasks — Мои задачи\n"
        parse_mode=ParseMode.HTML,
    )


@router.message(Command("all_tasks"), IsEngineer())
async def all_tasks_handler(message: Message):
    tasks = await get_all_tasks()
    for task in tasks:
        await message.answer(
            text=get_task_response(task), parse_mode=ParseMode.MARKDOWN_V2
        )


@router.message(Command("tasks_today"), IsEngineer())
async def task_today_handler(message: Message):
    tasks_today = await get_today_tasks()
    for task in tasks_today:
        if not task.get("started"):
            await message.answer(
                text=get_task_response(task),
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=get_accept_taks_id(task.get("task_id")),
            )


@router.message(Command("my_tasks"), IsEngineer())
async def my_tasks_handler(message: Message):
    tasks = await get_tasks_by_id(message.from_user.id)
    for task in tasks:
        await message.answer(
            text=get_task_response(task),
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=get_accept_taks_id(task.get("task_id")),
        )
