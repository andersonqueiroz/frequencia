from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from frequencia.core.messages import SuccessMessageMixin

from .models import Setor, Coordenadoria
from .forms import EditSetorForm, EditCoordenadoriaForm

#Views de setores
class SetoresCoordenadoriasListView(ListView):

 	model = Setor
 	template_name = 'setor_coordenadoria/setores_coordenadorias.html'

 	def get_context_data(self, **kwargs):
 		context = super(SetoresCoordenadoriasListView, self).get_context_data(**kwargs)
 		context['coordenadorias'] = Coordenadoria.objects.all()

 		return context


class SetorCreateView(SuccessMessageMixin, CreateView):

	model = Setor
	form_class = EditSetorForm
	template_name = 'setor_coordenadoria/setor_create_edit.html'

	success_message = 'Setor <b>%(nome)s</b> cadastrado com sucesso!'

	def get_success_url(self):
		return reverse('vinculos:setores_coordenadorias')


class SetorUpdateView(SuccessMessageMixin, UpdateView):

	model = Setor
	form_class = EditSetorForm
	template_name = 'setor_coordenadoria/setor_create_edit.html'	
	
	success_message = 'Setor <b>%(nome)s</b> atualizado com sucesso!'

	def get_success_url(self):
		return reverse('vinculos:setores_coordenadorias')


class CoordenadoriaCreateView(SuccessMessageMixin, CreateView):

	model = Coordenadoria
	form_class = EditCoordenadoriaForm
	template_name = 'setor_coordenadoria/coordenadoria_create_edit.html'

	success_message = 'Coordenadoria <b>%(nome)s</b> cadastrada com sucesso!'

	def get_success_url(self):
		return reverse('vinculos:setores_coordenadorias')


class CoordenadoriaUpdateView(SuccessMessageMixin, UpdateView):

	model = Coordenadoria
	form_class = EditCoordenadoriaForm
	template_name = 'setor_coordenadoria/coordenadoria_create_edit.html'
	
	success_message = 'Coordenadoria <b>%(nome)s</b> atualizada com sucesso!'

	def get_success_url(self):
		return reverse('vinculos:setores_coordenadorias')

# setores = SetoresListView.as_view()
setor_create = SetorCreateView.as_view()
setor_edit = SetorUpdateView.as_view()

# coordenadorias = CoordenadoriasListView.as_view()
coordenadoria_create = CoordenadoriaCreateView.as_view()
coordenadoria_edit = CoordenadoriaUpdateView.as_view()

setores_coordenadorias = SetoresCoordenadoriasListView.as_view()