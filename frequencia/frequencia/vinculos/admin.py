from django.contrib import admin

from .models import Setor, Coordenadoria, Bolsista
# Register your models here.

admin.site.register([Setor, Coordenadoria, Bolsista])
