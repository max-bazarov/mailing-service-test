# fabrique_test

## Описание

Coming soon

## Технологии
- Python 3.10.8
- Django REST Framework
- PostgreSQL
- Docker
- Nginx
- Gunicorn
- Celery

## Установка и запуск
- Склонируйте репозиторий на свой компьютер
- Измените файл .env.dist на .env и заполните его
- Убедитесь, что у вас установлен Docker и Docker Compose последних версий
- Запустите проект командой `docker-compose up`
- При первом запуске проекта необходимо выполнить миграции командой `docker-compose exec web python manage.py migrate`
- Создайте суперпользователя командой `docker-compose exec web python manage.py createsuperuser`
- Проект доступен по адресу http://localhost/

## Пример запросов
