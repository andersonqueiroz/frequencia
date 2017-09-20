from django.contrib import admin

from frequencia.vinculos.models import Vinculo

from .models import User

class VinculosInline(admin.TabularInline):
    model = Vinculo

class UsuarioAdmin(admin.ModelAdmin):
    inlines = [
        VinculosInline,
    ]

admin.site.register(User, UsuarioAdmin)



