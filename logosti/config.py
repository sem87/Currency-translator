# config.py
import os
from dataclasses import dataclass

import psycopg2
from dotenv import load_dotenv
from environs import Env
from sqlalchemy import create_engine


# from baze_sql import postgre_SQL
# Загружаем .env при старте
load_dotenv()


@dataclass
class DatabaseConfig:
    database_url: str


@dataclass
class Config:
    db: DatabaseConfig
    secret_key: str
    debug: bool
    sql_tabl: str


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)  # Загружаем переменные окружения из файла .env
    return Config(
        db=DatabaseConfig(database_url=env("DATABASE_URL")),
        secret_key=env("SECRET_KEY"),
        debug=env.bool("DEBUG", default=False),
        sql_tabl=env("SQL_TABL")
    )


def load_config_postgre() -> str:
    """Возвращает URL БЕЗ SSL-параметров — они будут в connect_args"""
    database_url = os.getenv("DATABASE_URL")
    # if database_url:
    #     # Удаляем старые SSL-параметры из URL, если есть
    #     if "?" in database_url:
    #         database_url = database_url.split("?")[0]
    return database_url

    # # Сборка из отдельных переменных
    # required = ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"]
    # if missing := [v for v in required if not os.getenv(v)]:
    #     raise ValueError(f"❌ Missing: {missing}")
    #
    # password = quote_plus(os.getenv("DB_PASSWORD"))
    # return (
    #     f"postgresql+psycopg2://"
    #     f"{os.getenv('DB_USER')}:{password}@"
    #     f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/"
    #     f"{os.getenv('DB_NAME')}"
    # )


def proverka():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        sslmode="require"  # Обязательно для Supabase!
    )
    print("✅ Подключено!")

    # Проверка: выполним простой запрос
    with conn.cursor() as cur:
        cur.execute("SELECT version();")
        print(f"📦 Версия PostgreSQL: {cur.fetchone()[0]}")
        print("начали добавлять")
        # new_user_postgre = postgre_SQL.Usersqlpostgre(name_fio="Семен", zam="это сама заметка", objasnenie="это обьяснение")
        # postgre_SQL.session1.add(new_user_postgre)
        # postgre_SQL.session1.commit()
        print("закончили")

    conn.close()
    print("🔌 Соединение закрыто")
    return (
        "postgresql+psycopg2://"
        "user:password@"  # ✅ Учетные данные
        "real-postgres-host.com:"  # ✅ Реальный хост PostgreSQL (не Cloudflare!)
        "5432/"  # ✅ Порт 5432
        "dbname"  # ✅ Имя базы
        "?sslmode=require"  # ✅ SSL для облаков
    )


def db_proverka():
    # Fetch variables
    USER = os.getenv("USER")
    PASSWORD = os.getenv("PASSWORD")
    HOST = os.getenv("HOST")
    PORT = os.getenv("PORT")
    DBNAME = os.getenv("DBNAME")
    # Construct the SQLAlchemy connection string
    DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"
    # Create the SQLAlchemy engine
    engine = create_engine(DATABASE_URL)
    # If using Transaction Pooler or Session Pooler, we want to ensure we disable SQLAlchemy client side pooling -
    # https://docs.sqlalchemy.org/en/20/core/pooling.html#switching-pool-implementations
    # engine = create_engine(DATABASE_URL, poolclass=NullPool)
    # Test the connection
    try:
        with engine.connect() as connection:
            print("Connection successful!")
    except Exception as e:
        print(f"Failed to connect: {e}")


if __name__ == "__main__":
    # proverka()
    # print(load_config_postgre())
    import requests as r

    my_ip = r.get("https://api.ipify.org", timeout=10).text
    print(f"🌍 Мой публичный IP: {my_ip}")
    for ip in ["207.254.46.208"]:
        res = r.get(f"http://{ip}:8000", timeout=10)
        print(f"Поменял  IP: {res}")
        print(f"✅ {ip} → {res.status_code}")
        db_proverka()
