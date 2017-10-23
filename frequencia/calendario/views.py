from rules.contrib.views import PermissionRequiredMixin, permission_required
from datetime import datetime

from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect

from frequencia.core.messages import SuccessMessageMixin

from .calendar import FeriadosRioGrandeDoNorte
from .models import FeriadoCalendarioAcademico
from .forms import CreateFeriadoForm


class FeriadoListView(LoginRequiredMixin, ListView):

	model = FeriadoCalendarioAcademico
	template_name = 'calendario/feriados.html'
	ano = datetime.now().year		

	def get_queryset(self):
		self.ano = self.kwargs.get('ano', self.ano)
		calendario = FeriadosRioGrandeDoNorte()
		try:
			return calendario.get_calendar_holidays(year=int(self.ano), with_id=True)
		except:
			self.ano = datetime.now().year
			return calendario.get_calendar_holidays(year=int(self.ano), with_id=True)

	def get_context_data(self, **kwargs):
		context = super(FeriadoListView, self).get_context_data(**kwargs)
		context['object_list'] = self.get_queryset()
		context['ano'] = self.ano
		context['form'] = CreateFeriadoForm
		return context

	def get_success_url(self):
		return self.request.META.get('HTTP_REFERER')

class FeriadoCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):

	model = FeriadoCalendarioAcademico
	form_class = CreateFeriadoForm
	permission_required = 'accounts.is_gestor'

	success_message = 'Feriado cadastrado com sucesso!'

	def get_success_url(self):
		return self.request.META.get('HTTP_REFERER')

	def render_to_response(self, context):		
		return redirect('calendario:feriados')		

@permission_required('accounts.is_gestor')
def feriado_remove(request, pk):

	feriado = get_object_or_404(FeriadoCalendarioAcademico, pk=pk)
	feriado.delete()
	messages.info(request, 'Feriado <b>%s</b> excluído com sucesso!' % feriado)
	return redirect(request.META.get('HTTP_REFERER'))


feriados = FeriadoListView.as_view()
feriado_create = FeriadoCreateView.as_view()