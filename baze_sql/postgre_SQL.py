from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, Float, Integer, String, create_engine, desc, text, event
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy.pool import QueuePool
from logs.config import *

engine = create_engine(load_config_postgre(), echo=True, pool_pre_ping=True,
                       connect_args={"sslmode": "prefer", "sslrootcert": None, "connect_timeout": 10})


class Base(DeclarativeBase):
    pass


# Переименуйте переменную, чтобы избежать конфликта имен
SessionLocal = sessionmaker(bind=engine)
session1 = SessionLocal()  # Используйте переименованную переменную


class Usersqlpostgre(Base):
    __tablename__ = 'otziv_sql_postgre'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    name_fio: Mapped[str] = mapped_column(String)
    zam: Mapped[str] = mapped_column(String)
    objasnenie: Mapped[str] = mapped_column(String)


Base.metadata.create_all(bind=engine)  # Эта строка создаст таблицу zeni

if __name__ == "__main__":
    new_user_postgre = Usersqlpostgre(name_fio="Семен", zam="это сама заметка", objasnenie="это обьяснение")
    session1.add(new_user_postgre)
    session1.commit()
