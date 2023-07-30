from django import template
import os

register = template.Library()

@register.filter(name='censor')
def censor(value, arg):
    with open('static/files/dict.txt', 'r', encoding='utf-8') as f:
        text = f.read()
        cens_text = str(value)
        for word in text.split():
            if word in cens_text:
                cens_text = cens_text.replace(str(word), '"not censor"')
        return cens_text

