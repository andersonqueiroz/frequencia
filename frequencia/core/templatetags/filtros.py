import os

from django import template

register = template.Library()

@register.filter(name='inverso')
def inverso(value):
	return value * -1

@register.filter
def filename(value):
	return os.path.basename(value.file.name)

@register.filter
def translate_boolean(value):
	return "Sim" if value else "Não"