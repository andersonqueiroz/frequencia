import datetime

from django.shortcuts import redirect
from django.views.generic.base import TemplateView

from frequencia.calendario.calendar import FeriadosRioGrandeDoNorte
from frequencia.vinculos.utils import get_bolsistas
from frequencia.vinculos.models import Vinculo
from frequencia.justificativas.models import JustificativaFalta
from frequencia.registro.models import Frequencia

def index(request):
	return redirect('registro:registro')

class HomeTemplateView(TemplateView):
	
	template_name = 'home.html'

	def __init__(self, **kwargs):
		super(HomeTemplateView, self).__init__(**kwargs)

		self.calendario = FeriadosRioGrandeDoNorte()
		self.data_atual = datetime.datetime.now()

	def dispatch(self, request, *args, **kwargs):
		self.bolsistas = get_bolsistas(self.request.user)
		return super(HomeTemplateView, self).dispatch(request, *args, **kwargs)

	def get_justificativas_pendentes(self):		
		return JustificativaFalta.objects.filter(status=0, vinculo__in=self.bolsistas).count()

	def get_registros_dia(self):
		data_hoje = self.data_atual.date()
		num_bolsistas_dia = Frequencia.objects.filter(created_at__date=data_hoje, 
													  tipo=0,
													  bolsista__in=self.bolsistas).count()
		return num_bolsistas_dia

	def get_context_data(self, **kwargs):
		context = super(HomeTemplateView, self).get_context_data(**kwargs)
		context['dias_uteis'] = self.calendario.count_working_days_month(self.data_atual.month, self.data_atual.year)
		context['justificativas'] = self.get_justificativas_pendentes() or None
		context['num_bolsistas'] = self.get_registros_dia()
		return context

home = HomeTemplateView.as_view()