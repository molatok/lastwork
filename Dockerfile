# Начинаем с базового образа Python
FROM python:3.10-slim

# Установка переменной окружения PYTHONUNBUFFERED в 1 для обеспечения вывода логов в реальном времени
ENV PYTHONUNBUFFERED 1

# Создание рабочей директории
WORKDIR /app

# Копирование файла зависимостей и установка зависимостей
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копирование всех файлов проекта в рабочую директорию
COPY . .

# Установка директории для сохранения статических файлов
RUN mkdir -p /app/staticfiles
ENV STATIC_ROOT /app/staticfiles

# Установка переменной окружения SECRET_KEY
ARG SECRET_KEY
ENV SECRET_KEY=$SECRET_KEY

# Запуск команды для сборки статических файлов
RUN python manage.py collectstatic --no-input

# Открываем порт для доступа к приложению
EXPOSE 8000

# Запуск команды для запуска сервера Django
CMD ["sh", "-c", "sleep 5 && python manage.py runserver 0.0.0.0:8000"]

