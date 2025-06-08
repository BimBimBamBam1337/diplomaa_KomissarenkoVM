from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column
from sqlalchemy import Integer, String


class Base(DeclarativeBase):
    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(30))
    first_name = mapped_column(String(30))
    midle_name = mapped_column(String, nullable=True)
    last_name = mapped_column(String(30))

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()


class Admins(Base): ...


class Professors(Base): ...


class Engineers(Base): ...
