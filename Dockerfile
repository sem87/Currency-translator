FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# VOLUME ["/app/semen","/app/books.db"]  # лучше указать в docker-compose
EXPOSE 8000
# Запускаем uvicorn напрямую (без reload для production)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug"]