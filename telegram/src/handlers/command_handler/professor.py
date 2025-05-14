from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from src.states import NewTask, FindTask
from src.filters import IsProfessor
from src.mongo import create_task, get_task_by_task_id
from src.utils import get_task_response

router = Router()


@router.message(Command("new_task"), IsProfessor())
async def new_task_handler(message: Message, state: FSMContext):
    await message.answer(
        text="📝 Введите название задачи:", parse_mode=ParseMode.MARKDOWN_V2
    )
    await state.set_state(NewTask.GetTaskName)


@router.message(NewTask.GetTaskName)
async def process_name_handler(message: Message, state: FSMContext):
    await state.update_data(task_name=message.text)
    await message.answer(
        text="📄 Введите описание задачи:", parse_mode=ParseMode.MARKDOWN_V2
    )
    await state.set_state(NewTask.GetTaskDisctiption)


@router.message(NewTask.GetTaskDisctiption)
async def process_description_handler(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer(
        text="⏳ Введите дедлайн в формате ДД.ММ.ГГГГ ЧЧ:ММ",
    )
    await state.set_state(NewTask.GetDeadline)


@router.message(NewTask.GetDeadline)
async def process_deadline_handler(message: Message, state: FSMContext):
    await state.update_data(deadline=message.text)
    data = await state.get_data()
    created_task = await create_task(
        professor_id=message.from_user.id,
        description=data.get("description"),
        task_name=data.get("task_name"),
        deadline=data.get("deadline"),
    )
    await message.answer(f"Идентификационный код ваше задачи:\n{created_task.task_id}")
    await state.clear()


@router.message(Command("find_task"), IsProfessor())
async def find_task_handler(message: Message, state: FSMContext):
    await message.answer("Введите идентификационный код вашей задачи:")
    await state.set_state(FindTask.OneTask)


@router.message(FindTask.OneTask)
async def send_task_handler(message: Message, state: FSMContext):
    task = await get_task_by_task_id(message.text)

    await message.answer(get_task_response(task), parse_mode=ParseMode.MARKDOWN_V2)
    await state.clear()
