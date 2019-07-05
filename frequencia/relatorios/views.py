from datetime import date, datetime, timedelta

from rules.contrib.views import PermissionRequiredMixin

from django.urls import reverse
from django.contrib import messages
from django.views.generic import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404

from frequencia.vinculos.models import Vinculo, Setor
from frequencia.vinculos.utils import get_bolsistas, get_setores

from .calculos import get_relatorio_mes, get_relatorio_mensal_setor, get_total_horas_registradas_contabilizadas
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

class BuscaRelatorioSetorTemplateView(PermissionRequiredMixin, FormView):

	template_name = 'relatorios/busca_setor.html'
	form_class = BuscaRelatorioSetorForm
	permission_required = 'accounts.is_servidor'

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

class RelatorioMensalDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):

	model = Vinculo
	template_name = 'relatorios/relatorio_mensal.html'
	permission_required = 'relatorio.can_view'

	def get_object(self):
		now = datetime.now()
		mes = int(self.request.GET.get('mes', now.month))
		ano = int(self.request.GET.get('ano', now.year))
		try:			
			self.periodo = date(day=1, month=mes, year=ano)
		except ValueError:
			self.periodo = date(day=1, month=now.month, year=now.year)

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
		context['horas_registradas_periodo'] = self.relatorio['horas_registradas_periodo']	
		context['horas_contabilizadas_periodo'] = self.relatorio['horas_contabilizadas_periodo']	
		context['horas_abonadas_periodo'] = self.relatorio['horas_abonadas_periodo']

		context['saldo_mes_anterior'] = self.relatorio['saldo_mes_anterior']			
		
		context['saldo_atual_mes'] = self.relatorio['total_horas_trabalhar'] \
									 + context['saldo_mes_anterior'] \
									 - self.relatorio['horas_contabilizadas_periodo'] \
									 - self.relatorio['horas_abonadas_periodo']	
	
		return context

	def render_to_response(self, context):
		if not self.relatorio:
			return redirect('relatorios:busca_relatorio')

		return super(RelatorioMensalDetailView, self).render_to_response(context)
	

class RelatorioSetorDetailView(PermissionRequiredMixin, DetailView):

	model = Setor
	template_name = 'relatorios/relatorio_setor.html'
	permission_required = 'relatorio.can_view_setor'	

	def get_context_data(self, **kwargs):
		now = datetime.now()
		ano = int(self.request.GET.get('ano', now.year))
		mes = int(self.request.GET.get('mes', now.month))
		try:
			self.periodo = date(ano, mes, 1)
		except ValueError:
			self.periodo = date(now.year, now.month, 1)

		context = super(RelatorioSetorDetailView, self).get_context_data(**kwargs)
		context['relatorio'] = get_relatorio_mensal_setor(self.object, self.periodo.month, self.periodo.year)
		context['periodo'] = self.periodo
		return context

class ListagemGeralListView(PermissionRequiredMixin, ListView):

	template_name = 'relatorios/listagem_geral.html'
	model = Vinculo
	permission_required = 'accounts.is_servidor'

	numero_dias = 7

	def get_queryset(self):
		bolsistas = get_bolsistas(self.request.user)
		dias = []

		for i in range(0, self.numero_dias):
			dia = datetime.now().date() - timedelta(days=i)		
			bolsistas_dia = bolsistas.filter(registros__created_at__date=dia).distinct()					

			if not bolsistas_dia:
				continue

			for bolsista in bolsistas_dia:
				bolsista.registros_dia = bolsista.registros_dia(dia)
				bolsista.horas_registradas, bolsista.horas_contabilizadas = get_total_horas_registradas_contabilizadas(
					bolsista.registros_dia
				)

			dias.append({'data':dia, 'bolsistas':bolsistas_dia})

		return dias

relatorio_mensal = RelatorioMensalDetailView.as_view()
busca_relatorio = BuscaRelatorioMensalTemplateView.as_view()
busca_setor = BuscaRelatorioSetorTemplateView.as_view()
listagem_geral = ListagemGeralListView.as_view()
relatorio_setor = RelatorioSetorDetailView.as_view()
