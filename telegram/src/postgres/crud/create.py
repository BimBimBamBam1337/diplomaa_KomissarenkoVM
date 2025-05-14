from typing import Type
from sqlalchemy import select
from loguru import logger

from ..models import Base
from .._engine import async_session


async def create_entity_if_not_exist(
    id_: int,
    username: str,
    first_name: str,
    last_name: str,
    midle_name: str | None,
    tablename: Type[Base],
):
    async with async_session() as session:
        exists = (
            await session.execute(
                select(tablename.id).where(tablename.id == id_).limit(1)
            )
        ).one_or_none()
        if exists is None:
            admin = tablename(
                id=id_,
                username=username,
                first_name=first_name,
                midle_name=midle_name,
                last_name=last_name,
            )
            session.add(admin)
            await session.commit()
            logger.info(f"REGISTRATE | Registrate in {tablename.__name__} - {id_}")
            return True
        else:
            logger.warning(f"EXIST | {tablename.__name__} already exists - {id_}")
            return False
