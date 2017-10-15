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

class RelatorioMensalDetailView(PermissionRequiredMixin, DetailView):

	model = Vinculo
	template_name = 'relatorios/relatorio_mensal.html'
	permission_required = 'relatorio.can_view'

	def dispatch(self, *args, **kwargs):
		try:
			mes = int(self.request.GET.get('mes', timezone.now().date().month))
			ano = int(self.request.GET.get('ano', timezone.now().date().year))
			self.periodo = date(day=1, month=mes, year=ano)
		except ValueError:
			messages.error(self.request, 'Data informada é inválida!')
			return redirect(reverse('relatorios:busca_relatorio'))

		return super(RelatorioMensalDetailView, self).dispatch(*args, **kwargs)

	def get_object(self):
		if 'pk' in self.kwargs:
			return super(RelatorioMensalDetailView, self).get_object()

		return self.request.user.vinculos.filter(group__name='Bolsista', ativo=True).first()	
	
	def get_context_data(self, **kwargs):
		context = super(RelatorioMensalDetailView, self).get_context_data(**kwargs)	

		self.relatorio = get_relatorio_mes(self.object, self.periodo.month, self.periodo.year)
		if not self.relatorio:
			messages.warning(self.request, 'Não há registros ou ausências no período informado.')			
			return context

		context['periodo'] = self.periodo
		context['bolsista'] = self.object
		context['lista_dias'] = self.relatorio['registros']
		context['dias_uteis'] = self.relatorio['dias_uteis']		
		context['total_horas_trabalhar'] = self.relatorio['total_horas_trabalhar']
		context['horas_trabalhadas_periodo'] = self.relatorio['horas_trabalhadas_periodo']	
		context['horas_abonadas_periodo'] = self.relatorio['horas_abonadas_periodo']

		context['saldo_mes_anterior'] = timedelta()
		if self.relatorio['saldo_mes_anterior'].days > 0:
			context['saldo_mes_anterior'] = self.relatorio['saldo_mes_anterior']		
		
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

	def render_to_response(self, context):
		if not self.relatorio:
			return redirect('relatorios:busca_relatorio')

		return super(RelatorioMensalDetailView, self).render_to_response(context)
	

class RelatorioSetorDetailView(DetailView):

	model = Setor
	template_name = 'relatorios/relatorio_setor.html'

	def dispatch(self, *args, **kwargs):
		try:
			mes = int(self.request.GET.get('mes', timezone.now().date().month))
			ano = int(self.request.GET.get('ano', timezone.now().date().year))
			self.periodo = date(ano, mes, 1)
		except ValueError:
			messages.error(self.request, 'Data informada é inválida!')
			return redirect(reverse('relatorios:busca_setor'))

		return super(RelatorioSetorDetailView, self).dispatch(*args, **kwargs)	

	def get_context_data(self, **kwargs):
		context = super(RelatorioSetorDetailView, self).get_context_data(**kwargs)	
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

relatorio_mensal = RelatorioMensalDetailView.as_view()
busca_relatorio = BuscaRelatorioMensalTemplateView.as_view()
busca_setor = BuscaRelatorioSetorTemplateView.as_view()
listagem_geral = ListagemGeralTemplateView.as_view()
relatorio_setor = RelatorioSetorDetailView.as_view()
