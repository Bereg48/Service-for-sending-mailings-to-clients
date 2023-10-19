from django.db import models

from config import settings
from message.models import Message

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    """Модель клиента"""
    name = models.CharField(max_length=150, verbose_name='Фамилия Имя Отчество')
    email = models.EmailField(unique=True, verbose_name='Почта')
    message = models.TextField(verbose_name='Комментарий', **NULLABLE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='Активность')

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
        ordering = ('name',)

    def __str__(self):
        return f"{self.name} ({self.email})"

    def delete(self, *args, **kwargs):
        """Функция, делающая пользователя не активным"""
        self.is_active = False
        self.save()




class Mailing(models.Model):
    """Модель рассылки"""

    FREQUENCY = [
        ('DAY', 'раз в день'),
        ('WEEK', 'раз в неделю'),
        ('MONTH', 'раз в месяц')
    ]

    STATUS = [
        ('FINISH', 'завершена'),
        ('CREATE', 'создана'),
        ('START', 'запущена')
    ]

    time = models.TimeField(auto_now_add=True, verbose_name='Время рассылки')
    create_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    frequency = models.CharField(max_length=100, choices=FREQUENCY, verbose_name='Периодичность')
    status = models.CharField(max_length=100, choices=STATUS, verbose_name='Статус')
    client = models.ManyToManyField(Client, verbose_name='Клиент', blank=True)
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, verbose_name='Сообщение', **NULLABLE)
    finish_date = models.DateField(verbose_name='Дата завершения рассылки', default='2024-01-01')
    finish_time = models.TimeField(verbose_name='Время завершения рассылки', default='00:00')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE)
    is_published = models.BooleanField(default=True, verbose_name='Опубликован')

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        ordering = ('time',)

    def __str__(self):
        return f'Рассылка №{self.pk}'

    def delete(self, *args, **kwargs):
        """Функция, делающая пост не активным"""
        self.is_published = False
        self.status = 'FINISH'
        self.save()


class MailingLogs(models.Model):
    """Модель логов рассылки"""
    STATUS = [
        ('Success', 'успешно'),
        ('Failure', 'отказ')
    ]

    data_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время отправки')
    status = models.CharField(max_length=100, choices=STATUS, verbose_name='Статус попытки')
    server_response = models.TextField(verbose_name='Ответ почтового сервера', **NULLABLE)
    mailing = models.ForeignKey(Mailing, on_delete=models.SET_NULL, verbose_name='Рассылка', **NULLABLE)

    class Meta:
        verbose_name = 'лог отправки письма'
        verbose_name_plural = 'логи отправок писем'

    def __str__(self):
        return f'Лог {self.pk}'
