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

ARG POSTGRES_DB
ENV POSTGRES_DB=$POSTGRES_DB

ARG POSTGRES_USER
ENV POSTGRES_USER=$POSTGRES_USER

ARG POSTGRES_PASSWORD
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD

ARG POSTGRES_HOST
ENV POSTGRES_HOST=$POSTGRES_HOST

ARG POSTGRES_PORT
ENV POSTGRES_PORT =$POSTGRES_PORT

ARG SOCIAL_AUTH_VK_OAUTH2_KEY
ENV SOCIAL_AUTH_VK_OAUTH2_KEY=$SOCIAL_AUTH_VK_OAUTH2_KEY

ARG SOCIAL_AUTH_VK_OAUTH2_SECRET
ENV SOCIAL_AUTH_VK_OAUTH2_SECRET=$SOCIAL_AUTH_VK_OAUTH2_SECRET

# Запуск команды для сборки статических файлов
RUN python manage.py collectstatic --no-input

# Открываем порт для доступа к приложению
EXPOSE 8000

# Запуск команды для запуска сервера Django
CMD ["sh", "-c", "sleep 5 && python manage.py runserver 0.0.0.0:8000"]