from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

from src.filters import IsAdmin
from src.utils import get_entity_respone
from src.postgres.crud.read import get_entitys
from src.postgres.models import Admins, Professors

router = Router()


@router.message(Command("admin"), IsAdmin())
async def admin_handler(message: Message):
    await message.answer(
        text="""
🛠️ <b>Административные команды</b> 🛠️

<b>Добавление юзеров</b>
▫️ /add_engineers - Список всех инженеров
▫️ /add_professors - Список всех инженеров

<b>Удаление юзеров</b>
▫️ /delete_engineers - Список всех инженеров
▫️ /delete_professors - Список всех инженеров

<b>Управление пользователями</b>
▫️ /list_engineers - Список всех инженеров
▫️ /list_professors - Список всех преподавателей
▫️ /find_user &lt;id/username&gt; - Поиск пользователя

/reassign &lt;task_id&gt; &lt;engineer_id&gt; - Переназначить задачу

<b>Системные команды</b>
▫️ /broadcast &lt;text&gt; - Рассылка сообщения
""",
        parse_mode=ParseMode.HTML,
    )


@router.message(Command("add_engineer"), IsAdmin())
async def add_engineers_handler(message: Message):
    await message.answer(text="Введите тэг пользователя (@пример):")
    admins = await Admins
    for admin in admins:
        await message.answer(text=get_entity_respone(admin))


@router.message(Command("add_professor"), IsAdmin())
async def add_professors_handler(message: Message):
    admins = await get_entitys(Admins)
    for admin in admins:
        await message.answer(text=get_entity_respone(admin))


@router.message(Command("delete_engineer"), IsAdmin())
async def delete_engineers_handler(message: Message):
    admins = await get_entitys(Admins)
    for admin in admins:
        await message.answer(text=get_entity_respone(admin))


@router.message(Command("delete_professor"), IsAdmin())
async def delete_professors_handler(message: Message):
    admins = await get_entitys(Admins)
    for admin in admins:
        await message.answer(text=get_entity_respone(admin))


@router.message(Command("list_professors"), IsAdmin())
async def list_professors_handler(message: Message):
    admins = await get_entitys(Admins)
    for admin in admins:
        await message.answer(text=get_entity_respone(admin))


@router.message(Command("list_engineers"), IsAdmin())
async def list_engineers_handler(message: Message):
    professors = await get_entitys(Professors)
    for professor in professors:
        await message.answer(text=get_entity_respone(professor))
