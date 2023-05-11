FROM python:3.10-slim

ENV PYTHONBUFFERED 1

WORKDIR todolist/
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD python manage.py runserver 0.0.0.0:8000