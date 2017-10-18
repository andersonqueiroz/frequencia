from django import template

register = template.Library()

@register.filter(name='inverso')
def inverso(value):
	return value * -1