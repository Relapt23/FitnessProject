from pydantic import BaseModel
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, Session, mapped_column, Mapped, DeclarativeBase, relationship
from typing import Annotated, Optional, List, Any

intpk = Annotated[int, mapped_column(primary_key=True)]

class User(BaseModel):
    username: str
    password: str

class ChooseExercises(BaseModel):
    muscles_types_id: List[int]

class UserRequest(BaseModel):
    id: int
    title: str
    intensity: str


class Base(DeclarativeBase):
    pass

# пользователи
class Users(Base):
    __tablename__ = "users"
    id: Mapped [int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str]
    password: Mapped[str]
    # exceptions: Mapped[str]

# Список упражнений
class Exercises(Base):
    __tablename__ = "exercises"
    id: Mapped [intpk]
    type: Mapped[int] = mapped_column(ForeignKey('muscle_types.id'))
    title: Mapped[str]
    youtube: Mapped[str]

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


# Комбинации групп мышц для составления тренировки
class CombinationsMusclesTypes(Base):
    __tablename__ = "combinations_muscles_types"
    id: Mapped [intpk]
    title: Mapped[str]
    intensity: Mapped[int] = mapped_column(ForeignKey('intensity.id'))


# Перечень упражнений для комбинаций групп мышц
class Workouts(Base):
    __tablename__ = "workouts"
    id: Mapped [intpk]
    exercise: Mapped[str]
    intensity: Mapped[int] = mapped_column(ForeignKey('intensity.id'))
    periodicity: Mapped[str]
    combination_id:  Mapped[int] = mapped_column(ForeignKey('combinations_muscles_types.id'))
    training_number: Mapped[int]



