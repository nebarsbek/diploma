# Используем официальный образ с uv
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы управления зависимостями
COPY pyproject.toml uv.lock ./

# Устанавливаем зависимости
# --frozen: использовать версии из uv.lock
# --no-install-project: не устанавливать сам проект как пакет (пока)
RUN uv sync --frozen --no-install-project

# Копируем код приложения
COPY . .

# Устанавливаем переменные окружения для Python
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Открываем порт
EXPOSE 8000

# Запускаем приложение через uv run
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
