## Пользователи
- Создание пользователя
POST /api/v1/users
```
{
    "phone_number": "79116551368",
    "tag": "java-tips",
    "time_zone": "Europe/Moscow"
}
```
При создании пользователя код оператора определяется автоматически по номеру телефона.
Телефон должен быть в формате 7XXXXXXXXXX(11 цифр), где X - цифра от 0 до 9.

- Просмотр всех пользователей
GET /api/v1/users
```
[
    {
        "phone_number": "79114048095",
        "operator_code": "911",
        "tag": "Python-tips",
        "time_zone": "Europe/Moscow"
    },
    
    ...
]
```
## Рассылки
- Создание рассылки
POST /api/v1/mailings
```
{
    "filter": {
        "operator_code": "911",
        "tag": "python-tips"
    },
    "message": "New cool python tip",
    "start_at": "20.12.2022 16:10",
    "end_at": "20.12.2022 16:20"
}
```
При создании рассылки нужно обязательно указать фильтр по тегу и коду оператора.
Время начала и окончания рассылки должно быть в формате "dd.mm.yyyy hh:mm".
Начало и окончание рассылки должно быть в будущем.

### Статистика

- Просмотреть все рассылки
GET /api/v1/mailings
```
[
    {
        "message": "Hello",
        "start_at": "20.12.2022 16:48:00",
        "end_at": "20.12.2022 16:50:00",
        "filter": {
            "tag": "java-tips",
            "operator_code": "953"
        },
        "message_count": {
            "not_sent": 0,
            "sent": 8,
            "failed": 0
        }
    },

    ...
]
```
У каждой рассылки есть статистика по количеству сообщений с группировкой по статусам:
- not_sent - не отправлено
- sent - отправлено
- failed - не отправлено из-за ошибки

- Просмотреть статистику по конкретной рассылке
GET /api/v1/mailings/<id>/stats
```
[
    {
        "id": 9,
        "status": "sent",
        "sent_at": "20.12.2022 17:00:00",
        "client": 
        {
            "phone_number": "79114048095",
            "operator_code": "911",
            "tag": "Python-tips",
            "time_zone": "Europe/Moscow"
        }
    },

    ...
]
```

