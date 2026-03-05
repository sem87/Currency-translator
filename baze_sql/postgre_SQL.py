import requests as r
from sqlalchemy import Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from logs.config import *


# engine = create_engine(load_config_postgre(), echo=True)
engine = create_engine(os.getenv("DATABASE_URL"), echo=True,future=True)

# Переименуйте переменную, чтобы избежать конфликта имен
SessionLocal = sessionmaker(bind=engine,autocommit=False,autoflush=False,expire_on_commit=False)
session1 = SessionLocal()  # Используйте переименованную переменную


class Base(DeclarativeBase):
    pass


class Usersqlpostgre(Base):
    __tablename__ = 'otziv_sql_postgre'
    id: Mapped[int] = mapped_column(Integer, primary_key=True,index=True,autoincrement=True)
    # created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    name_fio: Mapped[str] = mapped_column(String)
    zam: Mapped[str] = mapped_column(String)
    objasnenie: Mapped[str] = mapped_column(String)


Base.metadata.create_all(bind=engine)  # Эта строка создаст таблицу zeni

if __name__ == "__main__":
    print("начало")
    for ip in ["37.203.37.94", "173.245.49.151", "141.101.121.51", "23.227.39.129"]:
        print("продолжим")
        try:
            res = r.get(f"http://{ip}:80", timeout=10)
            print(f"✅ {ip} → {res.status_code}")
            new_user_postgre = Usersqlpostgre(name_fio="Семен", zam="это сама заметка", objasnenie="это обьяснение")
            session1.add(new_user_postgre)
            session1.commit()

        except:
            print(f"❌ {ip} → недоступен")
        # 🔌 Соединение закрывается автоматически
