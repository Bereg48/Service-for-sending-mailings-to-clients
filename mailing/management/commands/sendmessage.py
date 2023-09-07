from django.core.management import BaseCommand
from mailing.models import Mailing
from mailing.services.services import send_mailing


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('mailing_id', nargs=1, type=int)

    def handle(self, *args, **options) -> None:
        for mailing_id in options['mailing_id']:
            try:
                mailing = Mailing.objects.get(pk=mailing_id)
                send_mailing(mailing)
            except Exception:
                raise (f'Рассылка не существует')
