from datetime import date

from rules.contrib.views import PermissionRequiredMixin

from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404

from frequencia.vinculos.models import Vinculo, Coordenadoria, Setor

from .calculos import get_relatorio_mes
from .forms import BuscaRelatorioForm

class BuscaRelatorioMensalTemplateView(LoginRequiredMixin, FormView):

	template_name = 'relatorios/busca_relatorio.html'
	form_class = BuscaRelatorioForm

	def get_bolsistas(self):
		bolsistas = Vinculo.objects.filter(group__name='Bolsista', ativo=True).order_by('setor')

		user = self.request.user

		if user.is_superuser or user.has_perm('accounts.is_gestor'):
			return bolsistas.all()

		elif user.has_perm('accounts.is_coordenador_chefe'):
			vinculos = user.vinculos.filter(ativo=True)
			vinculos = vinculos.filter(Q(group__name='Coordenador') | Q(group__name='Chefe de setor'))

			coordenadorias = Coordenadoria.objects.filter(vinculos__in=vinculos)
			setores = Setor.objects.filter(Q(coordenadoria__in=coordenadorias) | Q(vinculos__in=vinculos))

			bolsistas = bolsistas.filter(setor__in=setores)
		else:
			bolsistas = None

		return bolsistas

	def get_form_kwargs(self):
		kwargs = super(BuscaRelatorioMensalTemplateView, self).get_form_kwargs()
		kwargs.update({
		     'vinculos' : self.get_bolsistas()
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

		try:
			self.mes = int(self.request.GET.get('mes', timezone.now().date().month))
			self.ano = int(self.request.GET.get('ano', timezone.now().date().year))
			date(self.ano, self.mes, 1)
		except ValueError:
			messages.error(self.request, 'Data informada é inválida!')
			return redirect(reverse('relatorios:busca_relatorio'))

		return super(RelatorioMensalTemplateView, self).dispatch(*args, **kwargs)

	def get_object(self):		
		print(self.bolsista)
		return self.bolsista

	def get_context_data(self, **kwargs):
		context = super(RelatorioMensalTemplateView, self).get_context_data(**kwargs)

		relatorio = get_relatorio_mes(self.bolsista, self.mes, self.ano)
		context['periodo'] = date(day=1, month=self.mes, year=self.ano)
		context['bolsista'] = self.bolsista
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

		if porcentagem_horas_abonadas > 100 - porcentagem_horas_trabalhadas:
			context['porcentagem_horas_abonadas'] = 100 - porcentagem_horas_trabalhadas
		else:
			context['porcentagem_horas_abonadas'] = porcentagem_horas_abonadas

		return context

relatorio_mensal = RelatorioMensalTemplateView.as_view()
busca_relatorio = BuscaRelatorioMensalTemplateView.as_view()
