# postgre_SQL.py
import os
import sys
from datetime import UTC, datetime
from urllib.parse import quote_plus

from dotenv import load_dotenv


# Загружаем .env ПЕРЕД использованием os.getenv()
# Явно указываем путь, если файл не в корне проекта
load_dotenv()  # или load_dotenv(".env")


# === 1. Функция получения строки подключения ===
def load_config_postgre() -> str:
    """Возвращает строку подключения для SQLAlchemy"""
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        # Убираем query-параметры из URL — SSL зададим через connect_args
        if "?" in database_url:
            database_url = database_url.split("?")[0]
        return database_url

    # Сборка из отдельных переменных
    required = ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"]
    missing = [var for var in required if not os.getenv(var)]
    if missing:
        raise ValueError(f"❌ Не найдены переменные окружения: {missing}")

    # Кодируем пароль на случай спецсимволов
    password = quote_plus(os.getenv("DB_PASSWORD"))

    return (
        f"postgresql+psycopg2://"
        f"{os.getenv('DB_USER')}:{password}@"
        f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/"
        f"{os.getenv('DB_NAME')}"
    )


# === 2. Импорт SQLAlchemy ПОСЛЕ загрузки .env ===
from sqlalchemy import DateTime, Integer, String, create_engine, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


# === 3. Создание engine с правильными SSL-настройками ===
try:
    # Попробуем использовать certifi для сертификатов
    import certifi

    ssl_config = {
        "sslmode": "require",
        "sslrootcert": certifi.where(),  # ✅ Путь к CA-сертификатам
        "connect_timeout": 10,
    }
    print(f"🔐 Используем SSL-сертификаты из: {certifi.where()}")
except ImportError:
    # Fallback без явного сертификата
    ssl_config = {
        "sslmode": "require",
        "connect_timeout": 10,
    }
    print("⚠️ certifi не установлен, используем базовый SSL")

engine = create_engine(
    load_config_postgre(),
    echo=True,  # Логирование SQL (отключите в продакшене)
    pool_pre_ping=True,  # Проверка "живости" соединения
    pool_size=3,  # Оптимально для Supabase pooler
    max_overflow=5,
    connect_args=ssl_config
)


# === 4. ORM модели ===
class Base(DeclarativeBase):
    pass


class Usersqlpostgre(Base):
    __tablename__ = 'otziv_sql_postgre'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC)
    )
    name_fio: Mapped[str] = mapped_column(String)
    zam: Mapped[str] = mapped_column(String)
    objasnenie: Mapped[str] = mapped_column(String)

    def __repr__(self):
        return f"<Usersqlpostgre(id={self.id}, name='{self.name_fio}')>"


# === 5. Фабрика сессий (НЕ создаём сессию глобально!) ===
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    """Контекстный менеджер для сессии"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# === 6. Тест подключения ===
def test_connection():
    """Проверяет, что можем подключиться к Supabase"""
    try:
        print("🔄 Тест подключения к Supabase...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.scalar()
            print("✅ Подключено!")
            print(f"📦 PostgreSQL: {version[:60]}...")
        return True
    except Exception as e:
        print(f"❌ Ошибка подключения: {type(e).__name__}: {e}")
        return False


# === 7. Основная функция ===
def main():
    if not test_connection():
        print("\n💡 Советы по исправлению:")
        print("1. Убедитесь, что проект в Supabase активен (не 'Paused')")
        print("2. Проверьте DB_USER: формат postgres.REF (20 символов)")
        print("3. Используйте Session pooler: *.pooler.supabase.com:5432")
        print("4. Установите certifi: pip install certifi")
        print("5. Попробуйте запустить debug_ssl.py (см. ниже)")
        return

    try:
        # Создаём таблицы (безопасно: если есть — не пересоздаёт)
        print("\n🏗️  Создаю таблицы...")
        Base.metadata.create_all(bind=engine)
        print("✅ Таблицы готовы")

        # Добавляем запись через контекстный менеджер
        print("\n💾 Добавляю тестовую запись...")
        with SessionLocal() as session:
            new_record = Usersqlpostgre(
                name_fio="Семен",
                zam="это сама заметка",
                objasnenie="это объяснение"
            )
            session.add(new_record)
            session.commit()
            # Refresh чтобы получить ID после INSERT
            session.refresh(new_record)
            print(f"✅ Запись добавлена! ID: {new_record.id}")

        # Читаем запись обратно
        with SessionLocal() as session:
            result = session.query(Usersqlpostgre).filter_by(name_fio="Семен").first()
            if result:
                print(f"📖 Прочитано: {result}")

    except Exception as e:
        print(f"❌ Ошибка при работе с БД: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Устанавливаем кодировку для Windows-консоли
    if sys.platform == "win32":
        os.system("chcp 65001 >nul")  # UTF-8 в консоли
    main()
