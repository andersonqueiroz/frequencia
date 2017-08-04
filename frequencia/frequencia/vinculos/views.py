from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView

from .models import Setor, Coordenadoria
from .forms import EditSetorForm, EditCoordenadoriaForm

#Views de setores
class SetoresListView(ListView):

	model = Setor
	template_name = 'setor/setores.html'


class SetorCreateView(SuccessMessageMixin, CreateView):

	model = Setor
	form_class = EditSetorForm
	template_name = 'setor/setor_create.html'

	success_message = 'Setor <b>%(nome)s</b> cadastrada com sucesso!'

	def get_success_url(self):
		return reverse('vinculos:setores')


class SetorUpdateView(SuccessMessageMixin, UpdateView):

	model = Setor
	form_class = EditSetorForm
	template_name = 'setor/setor_edit.html'	
	
	success_message = 'Setor <b>%(nome)s</b> atualizada com sucesso!'

	def get_success_url(self):
		return reverse('vinculos:setores')


#Views de Coordenadorias
class CoordenadoriasListView(ListView):

	model = Coordenadoria
	template_name = 'coordenadoria/coordenadorias.html'


class CoordenadoriaCreateView(SuccessMessageMixin, CreateView):

	model = Coordenadoria
	form_class = EditCoordenadoriaForm
	template_name = 'coordenadoria/coordenadoria_create.html'

	success_message = 'Coordenadoria <b>%(nome)s</b> cadastrada com sucesso!'

	def get_success_url(self):
		return reverse('vinculos:coordenadorias')


class coordenadoriaUpdateView(SuccessMessageMixin, UpdateView):

	model = Coordenadoria
	form_class = EditCoordenadoriaForm
	template_name = 'coordenadoria/coordenadoria_edit.html'	
	
	success_message = 'Coordenadoria <b>%(nome)s</b> atualizada com sucesso!'

	def get_success_url(self):
		return reverse('vinculos:coordenadorias')

# Create your views here.
def atribuir_vinculo(self, pk):
	pass

setores = SetoresListView.as_view()
setor_create = SetorCreateView.as_view()
setor_edit = SetorUpdateView.as_view()

coordenadorias = CoordenadoriasListView.as_view()
coordenadoria_create = CoordenadoriaCreateView.as_view()
coordenadoria_edit = coordenadoriaUpdateView.as_view()