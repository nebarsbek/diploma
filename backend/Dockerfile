# Используем официальный образ с uv
FROM python:3.12-slim-bookworm

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы управления зависимостями
COPY pyproject.toml uv.lock ./

# Устанавливаем uv
RUN pip install uv

# Устанавливаем зависимости
# --frozen: использовать версии из uv.lock
# --no-install-project: не устанавливать сам проект как пакет (пока)
RUN uv sync --frozen --no-install-project

# Копируем код приложения
COPY . .

# Устанавливаем переменные окружения для Python
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

# Открываем порт
EXPOSE 8000

# Запускаем приложение через uv run
CMD ["sh", "-c", "uv run alembic upgrade head && exec uv run uvicorn app.main:app --host 0.0.0.0 --port 8000"]
