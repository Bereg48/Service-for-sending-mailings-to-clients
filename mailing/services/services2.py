from mailing.models import Mailing, Client


def get_count_mailing():
    """Возвращает количество рассылок всего"""
    return Mailing.objects.count()


def get_active_mailing():
    """Возвращает количество активных рассылок"""
    return Mailing.objects.filter(status='START').count()


def get_unique_clients():
    """Возвращает количество уникальных клиентов для рассылок"""
    return Client.objects.values('email').distinct().count()
