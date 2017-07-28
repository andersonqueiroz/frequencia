from django.contrib import admin

# Register your models here.
from .models import Frequencia, Maquina

admin.site.register([Frequencia, Maquina])