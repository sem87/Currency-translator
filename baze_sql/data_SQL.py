from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, Float, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from logosti.config import *


engine = create_engine(load_config().sql_tabl, echo=True)  # echo - логирование SQL


class Base(DeclarativeBase):
    pass
# Переименуйте переменную, чтобы избежать конфликта имен
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()  # Используйте переименованную переменную


class Usersql(Base):
    __tablename__ = 'otzivisql'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name_fio: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    age: Mapped[int | None] = mapped_column(Integer)
    otziv: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC))


class Zeni(Base):
    __tablename__ = 'zeni'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    usd: Mapped[float] = mapped_column(Float)
    eur: Mapped[float] = mapped_column(Float)
    gbp: Mapped[float] = mapped_column(Float)
    cny: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC))

# Base.metadata.create_all(bind=engine)  # Эта строка создаст таблицу zeni
