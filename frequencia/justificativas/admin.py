from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

from .models import TipoJustificativaFalta, JustificativaFalta

class JustificativaAdmin(admin.ModelAdmin):
	list_filter = (
        ('inicio', DateFieldListFilter),
    )
	search_fields = ('vinculo__user__name', 'descricao', 'inicio', 'termino')


admin.site.register(JustificativaFalta, JustificativaAdmin)
admin.site.register([TipoJustificativaFalta])