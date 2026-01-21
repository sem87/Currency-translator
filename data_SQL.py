from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, create_engine, text, select, desc, \
    func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, backref, mapped_column, relationship, sessionmaker

from Core.config import *

engine = create_engine(load_config().sql_tabl, echo=True)  # echo - логирование SQL


class Base(DeclarativeBase):
    pass


# Base.metadata.create_all(bind=engine)

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
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))


class Zeni(Base):
    __tablename__ = 'zeni'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    usd: Mapped[float] = mapped_column(Float)
    eur: Mapped[float] = mapped_column(Float)
    gbp: Mapped[float] = mapped_column(Float)
    cny: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

# Base.metadata.create_all(bind=engine)  # Эта строка создаст таблицу zeni
