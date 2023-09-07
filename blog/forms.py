from django import forms
from django.conf import settings

from blog.models import Blog


class MixinStyle:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class BlogForms(MixinStyle, forms.ModelForm):
    class Meta:
        model = Blog
        exclude = ('is_active', 'date_create')

    def clean_product_name(self):
        cleaned_name = self.cleaned_data['product_name']
        for word in settings.FORBIDDEN_WORDS:
            if word in cleaned_name:
                raise forms.ValidationError(f'Запрещено использовать слово {word}.')
            if word.title() in cleaned_name:
                raise forms.ValidationError(f'Запрещено использовать слово {word}.')
        return cleaned_name

    def clean_product_text(self):
        cleaned_text = self.cleaned_data['product_text']
        for word in settings.FORBIDDEN_WORDS:
            if word.title() in cleaned_text:
                raise forms.ValidationError(f'Запрещено использовать слово {word}.')
            if word in cleaned_text:
                raise forms.ValidationError(f'Запрещено использовать слово {word}.')
        return cleaned_text
