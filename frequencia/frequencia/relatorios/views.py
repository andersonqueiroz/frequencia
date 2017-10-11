from datetime import date, timedelta

from rules.contrib.views import PermissionRequiredMixin

from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404

from frequencia.vinculos.models import Vinculo
from frequencia.vinculos.utils import get_bolsistas

from .calculos import get_relatorio_mes, get_total_horas_trabalhadas
from .forms import BuscaRelatorioForm

class BuscaRelatorioMensalTemplateView(LoginRequiredMixin, FormView):

	template_name = 'relatorios/busca_relatorio.html'
	form_class = BuscaRelatorioForm

	def get_form_kwargs(self):
		kwargs = super(BuscaRelatorioMensalTemplateView, self).get_form_kwargs()
		kwargs.update({
		     'vinculos' : get_bolsistas(self.request.user)
		})
		return kwargs

	def form_valid(self, form):
		self.mes = form.cleaned_data['mes']
		self.ano = form.cleaned_data['ano']
		self.bolsista = form.cleaned_data['bolsista']

		return super(BuscaRelatorioMensalTemplateView, self).form_valid(form)

	def get_success_url(self):
		if self.bolsista:
			url = reverse('relatorios:relatorio_mensal', kwargs={'pk': self.bolsista.pk}) 
		else:
			url = reverse('relatorios:relatorio_mensal')

		return url + '?mes={0}&ano={1}'.format(self.mes, self.ano)

class RelatorioMensalTemplateView(PermissionRequiredMixin, TemplateView):

	template_name = 'relatorios/relatorio_mensal.html'
	permission_required = 'relatorio.can_view'

	def dispatch(self, *args, **kwargs):
		if 'pk' in self.kwargs:
			self.bolsista = get_object_or_404(Vinculo, pk=self.kwargs['pk'])
		else:			
			self.bolsista = self.request.user.vinculos.filter(group__name='Bolsista', ativo=True).first()
			if not self.bolsista:
				messages.error(self.request, 'Bolsista não informado!')
				return redirect(reverse('relatorios:busca_relatorio'))

		return super(RelatorioMensalTemplateView, self).dispatch(*args, **kwargs)

	def get_relatorio(self):	
		try:
			self.mes = int(self.request.GET.get('mes', timezone.now().date().month))
			self.ano = int(self.request.GET.get('ano', timezone.now().date().year))
			date(self.ano, self.mes, 1)
		except ValueError:
			messages.error(self.request, 'Data informada é inválida!')
			return redirect(reverse('relatorios:busca_relatorio'))

		relatorio = get_relatorio_mes(self.bolsista, self.mes, self.ano)

		if not relatorio:
			messages.warning(self.request, 'Não há registros ou ausências no período informado.')
			return redirect(reverse('relatorios:busca_relatorio'))

		return relatorio

	def get_object(self):
		return self.bolsista

	def get_context_data(self, **kwargs):
		context = super(RelatorioMensalTemplateView, self).get_context_data(**kwargs)	

		self.relatorio = self.get_relatorio()		

		context['periodo'] = date(day=1, month=self.mes, year=self.ano)
		context['bolsista'] = self.bolsista
		context['lista_dias'] = self.relatorio['registros']
		context['dias_uteis'] = self.relatorio['dias_uteis']		
		context['total_horas_trabalhar'] =  self.relatorio['total_horas_trabalhar']
		context['horas_trabalhadas_periodo'] = self.relatorio['horas_trabalhadas_periodo']	
		context['horas_abonadas_periodo'] = self.relatorio['horas_abonadas_periodo']

		if self.relatorio['saldo_mes_anterior'].days > 0:
			context['saldo_mes_anterior'] = self.relatorio['saldo_mes_anterior']
		else:
			context['saldo_mes_anterior'] = timedelta()

		#### DEBUG ####
		# context['saldo_mes_anterior'] = timedelta(hours=0)
		# self.relatorio['horas_trabalhadas_periodo'] = timedelta(hours=12)
		# context['horas_trabalhadas_periodo'] = timedelta(hours=12)

		
		context['saldo_atual_mes'] = self.relatorio['total_horas_trabalhar'] \
									 + context['saldo_mes_anterior'] \
									 - self.relatorio['horas_trabalhadas_periodo'] \
									 - self.relatorio['horas_abonadas_periodo']	

		if context['saldo_atual_mes'].days < 0:
			 context['credito_horas'] = context['saldo_atual_mes'] * -1

		porcentagem_horas_trabalhadas = int(self.relatorio['horas_trabalhadas_periodo'] * 100 / (self.relatorio['total_horas_trabalhar'] + context['saldo_mes_anterior']))
		porcentagem_horas_abonadas = int(self.relatorio['horas_abonadas_periodo'] * 100 / (self.relatorio['total_horas_trabalhar'] + context['saldo_mes_anterior']))

		context['porcentagem_horas_trabalhadas'] = porcentagem_horas_trabalhadas

		if porcentagem_horas_abonadas > 100 - porcentagem_horas_trabalhadas:
			context['porcentagem_horas_abonadas'] = 100 - porcentagem_horas_trabalhadas
		else:
			context['porcentagem_horas_abonadas'] = porcentagem_horas_abonadas

		return context

class ListagemGeralTemplateView(TemplateView):

	template_name = 'relatorios/listagem_geral.html'
	permission_required = 'relatorio.can_view'

	def get_context_data(self, **kwargs):
		context = super(ListagemGeralTemplateView, self).get_context_data(**kwargs)
		bolsistas = get_bolsistas(self.request.user)

		if bolsistas:
			for bolsista in bolsistas:
				bolsista.horas_trabalhadas = get_total_horas_trabalhadas(bolsista.registros_dia())

		context['bolsistas'] = bolsistas
		return context

relatorio_mensal = RelatorioMensalTemplateView.as_view()
busca_relatorio = BuscaRelatorioMensalTemplateView.as_view()
listagem_geral = ListagemGeralTemplateView.as_view()
