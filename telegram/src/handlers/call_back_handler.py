from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from aiogram import F, Router
from src.mongo import update_engineer_in_task

router = Router()


@router.callback_query(F.data.startswith("accept:"))
async def accept_handler(call: CallbackQuery):
    _, task_id = call.data.split(":")
    await update_engineer_in_task(int(task_id), call.from_user.id)
    await call.message.answer(
        text=f"Вы приняли задачу с ID: `{task_id}`", parse_mode=ParseMode.MARKDOWN_V2
    )
    await call.answer()
