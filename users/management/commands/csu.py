from django.conf import settings
from django.core.management import BaseCommand
from django.db import IntegrityError

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            user = User.objects.create_superuser(
                email=settings.SUPERUSER_EMAIL,
                password=settings.SUPERUSER_PASSWORD,
            )
        except IntegrityError:
            user = User.objects.get(email='andreyanovi@yandex.ru')
            if not user.check_password(settings.SUPERUSER_PASSWORD):
                user.set_password(settings.SUPERUSER_PASSWORD)
            self.stdout.write(self.style.NOTICE('User "%s" already exists' % user))
        else:
            self.stdout.write(self.style.SUCCESS('User "%s" successfully created' % user))
