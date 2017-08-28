from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView

from .models import Setor, Coordenadoria
from .forms import EditSetorForm, EditCoordenadoriaForm

#Views de setores
class SetoresCoordenadoriasListView(ListView):

 	model = Setor
 	template_name = 'setor_coord/setores-coords.html'

 	def get_context_data(self, **kwargs):
 		context = super(SetoresCoordenadoriasListView, self).get_context_data(**kwargs)
 		context['coordenadorias'] = Coordenadoria.objects.all()

 		return context


class SetorCreateView(SuccessMessageMixin, CreateView):

	model = Setor
	form_class = EditSetorForm
	template_name = 'setor/setor_create.html'

	success_message = 'Setor <b>%(nome)s</b> cadastrada com sucesso!'

	def get_success_url(self):
		return reverse('vinculos:setores_coords')


class SetorUpdateView(SuccessMessageMixin, UpdateView):

	model = Setor
	form_class = EditSetorForm
	template_name = 'setor/setor_edit.html'	
	
	success_message = 'Setor <b>%(nome)s</b> atualizada com sucesso!'

	def get_success_url(self):
		return reverse('vinculos:setores_coords')


class CoordenadoriaCreateView(SuccessMessageMixin, CreateView):

	model = Coordenadoria
	form_class = EditCoordenadoriaForm
	template_name = 'coordenadoria/coordenadoria_create.html'

	success_message = 'Coordenadoria <b>%(nome)s</b> cadastrada com sucesso!'

	def get_success_url(self):
		return reverse('vinculos:setores_coords')


class coordenadoriaUpdateView(SuccessMessageMixin, UpdateView):

	model = Coordenadoria
	form_class = EditCoordenadoriaForm
	template_name = 'coordenadoria/coordenadoria_edit.html'	
	
	success_message = 'Coordenadoria <b>%(nome)s</b> atualizada com sucesso!'

	def get_success_url(self):
		return reverse('vinculos:setores_coords')

# setores = SetoresListView.as_view()
setor_create = SetorCreateView.as_view()
setor_edit = SetorUpdateView.as_view()

# coordenadorias = CoordenadoriasListView.as_view()
coordenadoria_create = CoordenadoriaCreateView.as_view()
coordenadoria_edit = coordenadoriaUpdateView.as_view()

setoresCoords = SetoresCoordenadoriasListView.as_view()