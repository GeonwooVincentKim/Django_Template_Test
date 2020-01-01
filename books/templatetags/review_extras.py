import datetime

from books.models import Book
from django import template
from django.http import request
from django.shortcuts import render
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


def cut(value, arg):
    return value.replace(arg, '')


@register.filter
@stringfilter
def lower(value):
    return value.lower()


# @register.filter(need_autoescape=True)
# def initial_letter_filter(text, autoescape=None):
#     first, other = text[0], text[1:]
#     if autoescape:
#         esc = conditional_escape
#     else:
#         esc = lambda x: x
#     result = '<strong>%s</strong>%s' % (esc(first), esc(other))
#     return mark_safe(result)


@register.filter(expects_localtime=True)
def businesshours(value):
    try:
        return 9 <= value.hour < 17
    except AttributeError:
        return ''


@register.simple_tag(takes_context=True)
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)


