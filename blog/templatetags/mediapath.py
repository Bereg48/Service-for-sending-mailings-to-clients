from django import template
from django.conf import settings

register = template.Library()


@register.filter
def mediapath(file_path):
    return "{}{}".format(settings.MEDIA_URL, file_path)


@register.simple_tag
def mediapath(file_path):
    return "{}{}".format(settings.MEDIA_URL, file_path)
