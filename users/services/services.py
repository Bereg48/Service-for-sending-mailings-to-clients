from django.conf import settings
from django.core.mail import send_mail


def auth_send_mail(user_email, activation_url):
    send_mail(
        subject='Подтверждение почты',
        message=f'Для подтверждения регистрации перейдите по ссылке: http://127.0.0.1:8000{activation_url}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False
    )
