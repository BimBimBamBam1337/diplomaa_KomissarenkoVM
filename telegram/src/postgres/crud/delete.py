from sqlalchemy import delete, select
from loguru import logger

from ..models import Base
from .._engine import async_session


from typing import Type


async def delete_entity(model: Type[Base], id_: int):
    """
    Удаляет сущность по ID.

    Args:
        model: Класс модели (Admins, Engineers, Professors)
        id_: ID записи для удаления

    Returns:
        int: Количество удалённых строк
    """
    async with async_session() as session:
        await session.execute(delete(model).where(model.id == id_))
        await session.commit()
        logger.info(f"DELETE | Deleted in {model.__tablename__} - {id_}")
