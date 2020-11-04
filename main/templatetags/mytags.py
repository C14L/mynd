from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(needs_autoescape=False)
def render(text):
    text = conditional_escape(text)
    text = text.replace("\n\n", "</p><p>")
    text = text.replace("\n", "<br>")
    text = "<p>%s</p>" % text
    return mark_safe(text)
