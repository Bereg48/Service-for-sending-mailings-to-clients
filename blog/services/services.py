from datetime import datetime
import pytz
from django.core.mail import send_mail
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from config import settings
from mailing.models import MailingLogs


class MessageService:
    def __init__(self, mailing):
        self.mailing = mailing

    def create_task(self):
        """Создание периодической задачи"""
        crontab = self.crontab_create()
        PeriodicTask.objects.create(crontab=crontab, name=str(self.mailing), task='send_message',
                                    args=[self.mailing.pk])

    def crontab_create(self):
        """Создание CRONTAB для выполнения периодических задач"""
        minute = self.mailing.time.minute
        hour = self.mailing.time.hour

        if self.mailing.frequency == 'DAY':
            day_of_week = '*'
            day_of_month = '*'

        elif self.mailing.frequency == 'WEEK':
            day_of_week = self.mailing.create_date.weekday()
            day_of_month = '*'

        else:
            day_of_week = '*',
            day_of_month = self.mailing.create_date.day if self.mailing.create_date.day <= 28 else 28

        schedule, _ = CrontabSchedule.objects.get_or_create(minute=minute, hour=hour, day_of_week=day_of_week,
                                                            day_of_month=day_of_month, month_of_year='*')

        return schedule


def finish_task(mailing):
    """Возвращает True или False в зависимости от того, выполнилась ли задача"""
    end_time = f'{mailing.finish_date} {mailing.finish_time}'
    end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

    current_time = datetime.now(pytz.timezone('Europe/Moscow'))
    current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    return current_time > str(end_time)


def delete_task(mailing):
    """Удаление периодической задачи"""
    task = PeriodicTask.objects.get(name=str(mailing))
    task.delete()
    mailing.status = 'FINISH'
    mailing.save()


def send_mailing(mailing):
    """Отправка рассылки и создание лога рассылки"""
    message = mailing.message
    clients = mailing.client.all()
    for client in clients:
        try:
            send_mail(
                subject=message.header,
                message=message.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email]
            )
            mailing_log = MailingLogs(
                data_time=datetime.now(),
                status='Success',
                server_response='Сообщение успешно отправлено',
                mailing=mailing,
            )
            mailing_log.save()

        except Exception:
            mailing_log = MailingLogs(
                data_time=datetime.now(),
                status='Failure',
                server_response='Сообщение не отправлено!',
                mailing=mailing,
            )
            mailing_log.save()
