from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_accept_taks_id(task_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Принять", callback_data=f"accept:{task_id}")]
        ]
    )
