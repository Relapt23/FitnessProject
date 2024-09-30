from pydantic import BaseModel
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, Session, mapped_column, Mapped, DeclarativeBase
from typing import Annotated

intpk = Annotated[int, mapped_column(primary_key=True)]

class User(BaseModel):
    username: str
    password: str

class Base(DeclarativeBase):
    pass

# пользователи
class Users(Base):
    __tablename__ = "users"
    id: Mapped [int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str]
    password: Mapped[str]
    exceptions: Mapped[str]

# Список упражнений
class Exercises(Base):
    __tablename__ = "exercises"
    id: Mapped [intpk]
    type: Mapped[int] = mapped_column(ForeignKey('muscle_types.id'))
    title: Mapped[str]

# Группы мышц
class Muscle_types(Base):
    __tablename__ = "muscle_types"
    id: Mapped [intpk]
    title: Mapped[str]

# Интенсивность
class Intensity(Base):
    __tablename__ = "intensity"
    id: Mapped [intpk]
    intensity: Mapped[str]

# Выбранные упражнения
class Exercises_preset(Base):
    __tablename__ = "exercises_preset"
    exercises_id: Mapped [int] = mapped_column(ForeignKey('exercises.id'),primary_key=True)
    intensity: Mapped[int] = mapped_column(ForeignKey('intensity.id'), primary_key=True)
    periodicity: Mapped[str]

# Упражнения, исключенные пользователем
class Exceptions(Base):
    __tablename__ = "exceptions"
    id: Mapped [intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    exercises_id: Mapped[int] = mapped_column(ForeignKey('exercises.id'), primary_key=True)


# con = engine.connect()
# con.execute(exercises.insert().values(
# 
# con.commit()


