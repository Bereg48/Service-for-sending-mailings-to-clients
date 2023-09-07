## Сервис отправки рассылок клиентам

### Для запуска celery:
- celery -A config worker -l info  


### Для создания createsuperuser:
- python manage.py csu

### Для отправки рассылки из командной строки:
- python manage.py sendmessage N, где N - это PK рассылки (PK рассылки смотри в админке)