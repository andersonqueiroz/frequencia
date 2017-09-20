from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView

from .calendar import FeriadosRioGrandeDoNorte
from .models import FeriadoCalendarioAcademico
from .forms import CreateFeriadoForm


class FeriadoCreateListView(SuccessMessageMixin, CreateView):

	model = FeriadoCalendarioAcademico

	template_name = 'calendario/feriados.html'
	ano = timezone.now().date().year
	form_class = CreateFeriadoForm

	success_message = 'Feriado cadastrado com sucesso!'

	def get_queryset(self):
		self.ano = self.kwargs.get('ano', self.ano)
		calendario = FeriadosRioGrandeDoNorte()
		return calendario.get_calendar_holidays(year=int(self.ano), with_id=True)

	def get_context_data(self, **kwargs):
		context = super(FeriadoCreateListView, self).get_context_data(**kwargs)
		context['object_list'] = self.get_queryset()
		context['ano'] = self.ano
		return context

	def get_success_url(self):
		return self.request.META.get('HTTP_REFERER')


def feriado_remove(request, pk):

	feriado = get_object_or_404(FeriadoCalendarioAcademico, pk=pk)
	feriado.delete()
	messages.success(request, 'Feriado <b>%s</b> excluído com sucesso!' % feriado)
	return redirect(request.META.get('HTTP_REFERER'))


feriados = FeriadoCreateListView.as_view()
feriado_create = FeriadoCreateListView.as_view()