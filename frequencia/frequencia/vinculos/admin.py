from django.contrib import admin

from .models import Setor, Coordenadoria, Vinculo
# Register your models here.

admin.site.register([Setor, Coordenadoria, Vinculo])
