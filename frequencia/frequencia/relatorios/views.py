from datetime import date

from rules.contrib.views import PermissionRequiredMixin

from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView

from frequencia.vinculos.models import Vinculo

from .calculos import get_relatorio_mes

class RelatorioMensalTemplateView(TemplateView):

	template_name = 'relatorios/relatorio_mensal.html'
	#permission_required = 'tipo_justificativa.can_manage'

	def dispatch(self, *args, **kwargs):		
		self.mes = int(self.request.GET.get('mes', timezone.now().date().month))
		self.ano = int(self.request.GET.get('ano', timezone.now().date().year))
		self.user = self.request.user

		try:
			date(self.ano, self.mes, 1)
		except ValueError:
			messages.error(self.request, 'Data informada é inválida!')
			return redirect(reverse('core:home'))

		return super(RelatorioMensalTemplateView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(RelatorioMensalTemplateView, self).get_context_data(**kwargs)

		relatorio = get_relatorio_mes(self.user, self.mes, self.ano)
		context['periodo'] = date(day=1, month=self.mes, year=self.ano)
		context['lista_dias'] = relatorio['registros']
		context['dias_uteis'] = relatorio['dias_uteis']		
		context['total_horas_trabalhar'] =  relatorio['total_horas_trabalhar']
		context['horas_trabalhadas_periodo'] = relatorio['horas_trabalhadas_periodo']				
		context['horas_abonadas_periodo'] = relatorio['horas_abonadas_periodo']
		
		context['saldo_atual_mes'] = relatorio['total_horas_trabalhar'] \
									 - relatorio['horas_trabalhadas_periodo'] \
									 - relatorio['horas_abonadas_periodo']	

		if context['saldo_atual_mes'].days < 0:
			 context['credito_horas'] = context['saldo_atual_mes'] * -1

		porcentagem_horas_trabalhadas = int(relatorio['horas_trabalhadas_periodo'] * 100 / relatorio['total_horas_trabalhar'])
		porcentagem_horas_abonadas = int(relatorio['horas_abonadas_periodo'] * 100 / relatorio['total_horas_trabalhar'])

		context['porcentagem_horas_trabalhadas'] = porcentagem_horas_trabalhadas
		context['porcentagem_horas_abonadas'] = porcentagem_horas_abonadas

		if porcentagem_horas_abonadas > 100 - porcentagem_horas_trabalhadas:
			context['porcentagem_horas_abonadas'] = 100 - porcentagem_horas_trabalhadas

		return context

relatorio_mensal = RelatorioMensalTemplateView.as_view()
