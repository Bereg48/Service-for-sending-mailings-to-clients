from django.db import models

from config import settings

NULLABLE = {'blank': True, 'null': True}


class Message(models.Model):
    """Модель сообщения для рассылки"""
    header = models.CharField(max_length=100, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')
    is_published = models.BooleanField(default=True, verbose_name='Создано')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE)

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
        ordering = ('header',)

    def __str__(self):
        return self.header
