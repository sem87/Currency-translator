# redis_client.py
import redis
from environs import Env


env = Env()
env.read_env()

# Получаем настройки из окружения
REDIS_HOST = env.str("REDIS_HOST", "redis")  # Имя сервиса в docker-compose
REDIS_PORT = env.int("REDIS_PORT", 6379)
REDIS_DB = env.int("REDIS_DB", 0)
REDIS_TTL = env.int("REDIS_TTL", 300)  # Время жизни кеша в секундах (5 минут)

# Создаём клиент (синхронный)
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True,  # Автоматически декодирует bytes → str
    socket_connect_timeout=5
)


def check_redis_connection():
    """Проверка доступности Redis"""
    try:
        redis_client.ping()
        print("✓ Redis работает")
        return True
    except redis.ConnectionError as e:
        print(f"✗ Ошибка подключения к Redis: {e}")
        return False
    except redis.TimeoutError as e:
        print(f"✗ Таймаут подключения: {e}")
        return False


if __name__ == "__main__":
    print(f"Redis клиент: {redis_client}")
    check_redis_connection()
    print(f"Результат проверки: {check_redis_connection()}")
