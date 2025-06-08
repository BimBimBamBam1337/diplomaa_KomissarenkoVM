from typing import Optional, Type
from sqlalchemy import select
from loguru import logger

from ..models import Base
from .._engine import async_session

__all__ = ["get_entity"]


async def get_entity(
    tablename: Type[Base],
    user_id: Optional[int] = None,
    username: Optional[str] = None,
) -> Base:
    async with async_session() as session:
        if user_id:
            entity = (
                (
                    await session.execute(
                        select(tablename).where(tablename.id == user_id)
                    )
                )
                .scalars()
                .first()
            )

            return entity
        if username:
            entity = (
                (
                    await session.execute(
                        select(tablename).where(tablename.username == username)
                    )
                )
                .scalars()
                .first()
            )

            return entity


async def get_entitys(tablename: Type[Base]):
    async with async_session() as session:
        return (await session.execute(select(tablename))).scalars().all()
