# Сервис отправки рассылок клиентам

## Предназначение приложения:
- Создания писем рассылок и самих рассылок клиентам 
- Контроль доставки рассылок

### 1. Для запуска приложения необходимо настроить виртуальное окружение и установить все необходимые зависимости с помощью группы команд:
    Команда для Windows:
        1- python -m venv venv
        2- venv\Scripts\activate
        3- pip install -r requirement.txt

    Команда для Unix:
        1- python3 -m venv venv
        2- source venv/bin/activate 
        3- pip install -r requirement.txt

### 2. Для запуска celery:
        1- celery -A config worker --loglevel=info --pool=eventlet
        2- celery -A config beat -l info -s django

### 3. Для создания createsuperuser:
        1- python manage.py csu


### 4. Для работы с переменными окружениями необходимо заполнить файл
    - .env

### 5. Для отправки рассылки из командной строки:
        1- python manage.py sendmessage N, где N - это PK рассылки (PK рассылки смотри в админке)
