from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.postgres.crud import get_entity
from src.postgres import Admins, Professors, Engineers


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if await get_entity(Admins, message.from_user.id):
            return True
        return False


class IsProfessor(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if await get_entity(Professors, message.from_user.id):
            return True
        return False


class IsEngineer(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if await get_entity(Engineers, message.from_user.id):
            return True
        return False
