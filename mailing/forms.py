from django import forms

from mailing.models import Client, Mailing, Message


class FormStyleMixin:
    """Класс-миксин для стилизации форм"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ClientForm(FormStyleMixin, forms.ModelForm):
    """Форма для создания и редактирования поста"""

    class Meta:
        model = Client
        exclude = ('is_active', 'user')


class MailingForm(FormStyleMixin, forms.ModelForm):
    """Форма для создания и редактирования рассылки"""

    class Meta:
        model = Mailing
        exclude = ('is_active', 'user', 'status', 'is_published')


class MessageForm(FormStyleMixin, forms.ModelForm):
    """Форма для создания и редактирования сообщения"""

    class Meta:
        model = Message
        exclude = ('header', 'body')
