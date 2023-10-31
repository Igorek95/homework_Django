from django import template
from config.settings import MEDIA_URL
from os.path import join

register = template.Library()


@register.simple_tag
def mediapath(format_string):
    return join(MEDIA_URL, format_string.name)