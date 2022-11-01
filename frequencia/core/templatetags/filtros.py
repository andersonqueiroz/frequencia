import os

from django import template

register = template.Library()

@register.filter(name='inverso')
def inverso(value):
	return value * -1

@register.filter
def filename(value):
	return os.path.basename(value.file.name)