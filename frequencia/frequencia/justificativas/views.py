from django.urls import reverse
from django.contrib import messages
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView

from .models import TipoJustificativaFalta, JustificativaFalta
from .forms import EditTipoJustificativaForm

class TipoJustificativaListView(ListView):

	model = TipoJustificativaFalta
	template_name = 'tipo_justificativa/tipo-justificativa.html'


class TipoJustificativaCreateView(SuccessMessageMixin, CreateView):

	model = TipoJustificativaFalta
	form_class = EditTipoJustificativaForm
	template_name = 'tipo_justificativa/tipo-justificativa-create-edit.html'

	success_message = 'Tipo de justificativa cadastrado com sucesso!'

	def get_success_url(self):
		return reverse('justificativas:tipo_justificativa')


class TipoJustificativaUpdateView(SuccessMessageMixin, UpdateView):

	model = TipoJustificativaFalta
	form_class = EditTipoJustificativaForm
	template_name = 'tipo_justificativa/tipo-justificativa-create-edit.html'
	
	success_message = 'Tipo de justificativa atualizado com sucesso!'

	def get_success_url(self):
		return reverse('justificativas:tipo_justificativa')


def tipo_justificativa_remove(request, pk):

	tipo_justificativa = get_object_or_404(TipoJustificativaFalta, pk=pk)
	tipo_justificativa.delete()
	messages.success(request, 'Tipo de justificativa de falta excluído com sucesso!')
	return redirect('justificativas:tipo_justificativa')


tipo_justificativa = TipoJustificativaListView.as_view()
tipo_justificativa_create = TipoJustificativaCreateView.as_view()
tipo_justificativa_edit = TipoJustificativaUpdateView.as_view()