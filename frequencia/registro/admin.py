from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

# Register your models here.
from .models import Frequencia, Maquina

class FrequenciaAdmin(admin.ModelAdmin):
	list_filter = (
        ('created_at', DateFieldListFilter),
    )
	search_fields = ('bolsista__user__name', 'created_at', 'bolsista__setor__nome', 'bolsista__setor__coordenadoria__nome', )
	readonly_fields=('created_at', 'updated_at', )


admin.site.register(Frequencia, FrequenciaAdmin)

admin.site.register([Maquina])