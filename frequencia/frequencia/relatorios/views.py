from rules.contrib.views import PermissionRequiredMixin

from django.utils import timezone
from django.shortcuts import render
from django.views.generic.base import TemplateView

from frequencia.vinculos.models import Vinculo

from .calculos import get_relatorio_mes

class RelatorioMensalTemplateView(TemplateView):

	template_name = 'relatorios/mensal.html'
	#permission_required = 'tipo_justificativa.can_manage'

	def dispatch(self, *args, **kwargs):
		self.mes = int(self.request.GET.get('mes', timezone.now().date().month))
		self.ano = int(self.request.GET.get('ano', timezone.now().date().year))
		self.user = self.request.user

		return super(RelatorioMensalTemplateView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(RelatorioMensalTemplateView, self).get_context_data(**kwargs)

		relatorio = get_relatorio_mes(self.user, self.mes, self.ano)
		context['lista_dias'] = relatorio['registros']
		context['dias_uteis'] = relatorio['dias_uteis']
		context['total_horas_trabalhar'] =  relatorio['total_horas_trabalhar']
		context['horas_trabalhadas_periodo'] = relatorio['horas_trabalhadas_periodo']		
		context['horas_abonadas_periodo'] = relatorio['horas_abonadas_periodo']

		context['porcentagem_horas_trabalhadas'] = int(relatorio['horas_trabalhadas_periodo'] * 100 / relatorio['total_horas_trabalhar'])

		return context

relatorio_mensal = RelatorioMensalTemplateView.as_view()
