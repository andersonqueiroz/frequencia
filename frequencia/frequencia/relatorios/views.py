from datetime import date, timedelta

from rules.contrib.views import PermissionRequiredMixin

from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.views.generic import FormView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404

from frequencia.vinculos.models import Vinculo, Setor
from frequencia.vinculos.utils import get_bolsistas, get_setores

from .calculos import get_relatorio_mes, get_relatorio_mensal_setor, get_total_horas_trabalhadas
from .forms import BuscaRelatorioForm, BuscaRelatorioSetorForm

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

class BuscaRelatorioSetorTemplateView(LoginRequiredMixin, FormView):

	template_name = 'relatorios/busca_setor.html'
	form_class = BuscaRelatorioSetorForm

	def get_form_kwargs(self):
		kwargs = super(BuscaRelatorioSetorTemplateView, self).get_form_kwargs()
		kwargs.update({
		     'setores' : get_setores(self.request.user)
		})
		return kwargs

	def form_valid(self, form):
		self.mes = form.cleaned_data['mes']
		self.ano = form.cleaned_data['ano']
		self.setor = form.cleaned_data['setor']

		return super(BuscaRelatorioSetorTemplateView, self).form_valid(form)

	def get_success_url(self):		
		url = reverse('relatorios:relatorio_setor', kwargs={'pk': self.setor.pk})
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

		try:
			self.mes = int(self.request.GET.get('mes', timezone.now().date().month))
			self.ano = int(self.request.GET.get('ano', timezone.now().date().year))
			date(self.ano, self.mes, 1)
		except ValueError:
			messages.error(self.request, 'Data informada é inválida!')
			return redirect(reverse('relatorios:busca_relatorio'))

		return super(RelatorioMensalTemplateView, self).dispatch(*args, **kwargs)

	def get_object(self):
		return self.bolsista

	def get_context_data(self, **kwargs):
		context = super(RelatorioMensalTemplateView, self).get_context_data(**kwargs)	

		relatorio = get_relatorio_mes(self.bolsista, self.mes, self.ano)
		if not relatorio:
			messages.warning(self.request, 'Não há registros ou ausências no período informado.')
			return redirect(reverse('relatorios:busca_relatorio'))

		context['periodo'] = date(day=1, month=self.mes, year=self.ano)
		context['bolsista'] = self.bolsista
		context['lista_dias'] = relatorio['registros']
		context['dias_uteis'] = relatorio['dias_uteis']		
		context['total_horas_trabalhar'] = relatorio['total_horas_trabalhar']
		context['horas_trabalhadas_periodo'] = relatorio['horas_trabalhadas_periodo']	
		context['horas_abonadas_periodo'] = relatorio['horas_abonadas_periodo']

		if relatorio['saldo_mes_anterior'].days > 0:
			context['saldo_mes_anterior'] = relatorio['saldo_mes_anterior']
		else:
			context['saldo_mes_anterior'] = timedelta()

		#### DEBUG ####
		# context['saldo_mes_anterior'] = timedelta(hours=0)
		# self.relatorio['horas_trabalhadas_periodo'] = timedelta(hours=12)
		# context['horas_trabalhadas_periodo'] = timedelta(hours=12)

		
		context['saldo_atual_mes'] = relatorio['total_horas_trabalhar'] \
									 + context['saldo_mes_anterior'] \
									 - relatorio['horas_trabalhadas_periodo'] \
									 - relatorio['horas_abonadas_periodo']	

		if context['saldo_atual_mes'].days < 0:
			 context['credito_horas'] = context['saldo_atual_mes'] * -1

		porcentagem_horas_trabalhadas = int(relatorio['horas_trabalhadas_periodo'] * 100 / (relatorio['total_horas_trabalhar'] + context['saldo_mes_anterior']))
		porcentagem_horas_abonadas = int(relatorio['horas_abonadas_periodo'] * 100 / (relatorio['total_horas_trabalhar'] + context['saldo_mes_anterior']))

		context['porcentagem_horas_trabalhadas'] = porcentagem_horas_trabalhadas

		if porcentagem_horas_abonadas > 100 - porcentagem_horas_trabalhadas:
			context['porcentagem_horas_abonadas'] = 100 - porcentagem_horas_trabalhadas
		else:
			context['porcentagem_horas_abonadas'] = porcentagem_horas_abonadas

		return context

class RelatorioSetorTemplateView(DetailView):

	model = Setor
	template_name = 'relatorios/relatorio_setor.html'

	def dispatch(self, *args, **kwargs):
		try:
			mes = int(self.request.GET.get('mes', timezone.now().date().month))
			ano = int(self.request.GET.get('ano', timezone.now().date().year))
			self.periodo = date(ano, mes, 1)
		except ValueError:
			messages.error(self.request, 'Data informada é inválida!')
			return redirect(reverse('relatorios:busca_relatorio'))

		return super(RelatorioSetorTemplateView, self).dispatch(*args, **kwargs)	

	def get_context_data(self, **kwargs):
		context = super(RelatorioSetorTemplateView, self).get_context_data(**kwargs)	
		context['relatorio'] = get_relatorio_mensal_setor(self.object, self.periodo.month, self.periodo.year)
		context['periodo'] = self.periodo
		return context

class ListagemGeralTemplateView(TemplateView):

	template_name = 'relatorios/listagem_geral.html'	

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
busca_setor = BuscaRelatorioSetorTemplateView.as_view()
listagem_geral = ListagemGeralTemplateView.as_view()
relatorio_setor = RelatorioSetorTemplateView.as_view()
