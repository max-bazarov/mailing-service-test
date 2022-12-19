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
- Регистрация пользователя
```
POST /api/v1/auth/signup/
{
    "email": "test@test.com",
    "username": "test"
}
```
- Получение JWT-токена
```
POST /api/v1/auth/token/
{
    "username": "test",
    "confirmation_code": "12345"
}
```
- Получение списка всех категорий
```
GET /api/v1/categories/
```