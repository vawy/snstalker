# === STAGE 1: Builder (установка зависимостей через uv) ===
FROM python:3.11-slim AS builder

# Установка системных зависимостей (для компиляции пакетов вроде psycopg)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка uv через pip (более надёжно, чем скрипт)
RUN pip install --no-cache-dir uv

WORKDIR /app

# Копируем pyproject.toml, uv.lock и requirements.txt
COPY pyproject.toml uv.lock requirements.txt ./

# Создаём виртуальное окружение и устанавливаем зависимости в него
RUN uv venv /app/.venv && \
    uv pip install --no-cache-dir -r requirements.txt

# === STAGE 2: Runtime (финальный образ) ===
FROM python:3.11-slim AS runtime

# Установка runtime системных зависимостей (только для работы, не для сборки)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Создание пользователя
RUN useradd --create-home --shell /bin/bash app
USER app
WORKDIR /home/app

# Копируем виртуальное окружение из builder stage
COPY --from=builder --chown=app:app /app/.venv /home/app/.venv

# Добавляем виртуальное окружение в PATH и PYTHONPATH
ENV PATH=/home/app/.venv/bin:$PATH
ENV PYTHONPATH=/home/app/.venv/lib/python3.11/site-packages:$PYTHONPATH

# Копируем исходный код
COPY --chown=app:app . .

EXPOSE 8000

# CMD для продакшена (раскомментируй нужный)
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "snstalker_project.wsgi:application"]
CMD ["uvicorn", "snstalker_project.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
