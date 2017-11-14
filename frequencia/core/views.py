import datetime
from datetime import timedelta

from django.db.models import Count
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from frequencia.calendario.calendar import FeriadosRioGrandeDoNorte
from frequencia.vinculos.utils import get_bolsistas, get_setores
from frequencia.vinculos.models import Vinculo
from frequencia.justificativas.models import JustificativaFalta
from frequencia.registro.models import Frequencia
from frequencia.relatorios.calculos import get_balanco_mes, get_balanco_mes_anterior

def index(request):
	return redirect('registro:registro')

class HomeTemplateView(LoginRequiredMixin, TemplateView):	
	

	def __init__(self, **kwargs):
		super(HomeTemplateView, self).__init__(**kwargs)

		self.calendario = FeriadosRioGrandeDoNorte()
		self.data_atual = datetime.datetime.now()

	def dispatch(self, request, *args, **kwargs):		
		self.user = self.request.user				
		return super(HomeTemplateView, self).dispatch(request, *args, **kwargs)

	def get_bolsistas_por_setor(self):
		setores = get_setores(self.user)

		return Vinculo.objects.filter(group__name="Bolsista", 
						ativo=True, 
						user__is_active=True, 
						setor__in=setores).values('setor').annotate(bolsistas=Count('setor')).values('setor__pk', 'setor__nome', 'bolsistas')


	def get_justificativas_pendentes(self):
		return JustificativaFalta.objects.filter(status=0, vinculo__in=self.bolsistas).count()

	def get_ultimos_registros(self):
		return Frequencia.objects.filter(bolsista__in=self.bolsistas).order_by('-pk')[:10]

	def get_num_bolsistas_trabalhando(self):
		data_hoje = self.data_atual.date()
		num_bolsistas_dia = Frequencia.objects.filter(created_at__date=data_hoje, 
													  tipo=0,
													  bolsista__in=self.bolsistas).count()
		return num_bolsistas_dia

	def get_bolsas_expirando(self):
		hoje = datetime.datetime.now().date()
		dia_final = hoje + timedelta(days=90)
		print(dia_final)
		return self.bolsistas.filter(group__name='Bolsista', 
									 ativo=True,
									 termino_vigencia__lte=dia_final)

	def get_context_data(self, **kwargs):
		context = super(HomeTemplateView, self).get_context_data(**kwargs)
		self.bolsistas = get_bolsistas(self.user)

		context['dias_uteis'] = self.calendario.count_working_days_month(self.data_atual.month, self.data_atual.year)
		context['ultimos_registros'] = self.get_ultimos_registros()
		context['justificativas'] = self.get_justificativas_pendentes() or None

		if self.user.has_perm('accounts.is_servidor'):		
			self.template_name = 'home/home_servidor.html'	
			context['num_bolsistas_trabalhando'] = self.get_num_bolsistas_trabalhando()
			context['bolsas_expirando'] = self.get_bolsas_expirando()

			if self.user.has_perm('accounts.is_gestor_coordenador'):				
				context['bolsistas_por_setor'] = self.get_bolsistas_por_setor()
			elif self.user.has_perm('accounts.is_chefe'):						
				context['bolsistas_setor'] = self.bolsistas
		else:
			self.template_name = 'home/home_bolsista.html'
			bolsista = self.bolsistas.first()
			balanco_mes = get_balanco_mes(bolsista, self.data_atual.month, self.data_atual.year)
			balanco_mes_anterior = get_balanco_mes_anterior(bolsista, self.data_atual.month, self.data_atual.year)

			context['dados_bolsista'] = bolsista
			context['balanco_mes'] = balanco_mes + balanco_mes_anterior
			context['ultimos_registros'] = context['ultimos_registros'][:6]
		
		return context

home = HomeTemplateView.as_view()
