from django.utils import timezone
from django.shortcuts import render
from django.views.generic import ListView

from .calendar import FeriadosRioGrandeDoNorte
from .models import FeriadoCalendarioAcademico

#Views de setores
class FeriadosListView(ListView):

 	template_name = 'calendario/feriados.html'
 	ano_atual = timezone.now().date().year

 	def get_queryset(self):
 		ano = self.kwargs.get('ano', self.ano_atual)
 		calendario = FeriadosRioGrandeDoNorte()
 		return calendario.holidays(year=int(ano))		


feriados = FeriadosListView.as_view()