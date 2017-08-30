from django.urls import reverse
from django.http import HttpResponseRedirect 
from django.contrib import messages
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView

from .models import TipoJustificativaFalta, JustificativaFalta
from .forms import EditTipoJustificativaForm, EditJustificativaForm

#Tipos de justificativa
class TipoJustificativaListView(ListView):

	model = TipoJustificativaFalta
	template_name = 'tipo_justificativa/tipo_justificativa.html'


class TipoJustificativaCreateView(SuccessMessageMixin, CreateView):

	model = TipoJustificativaFalta
	form_class = EditTipoJustificativaForm
	template_name = 'tipo_justificativa/tipo_justificativa_create_edit.html'

	success_message = 'Tipo de justificativa cadastrado com sucesso!'

	def get_success_url(self):
		return reverse('justificativas:tipo_justificativa')


class TipoJustificativaUpdateView(SuccessMessageMixin, UpdateView):

	model = TipoJustificativaFalta
	form_class = EditTipoJustificativaForm
	template_name = 'tipo_justificativa/tipo_justificativa_create_edit.html'
	
	success_message = 'Tipo de justificativa atualizado com sucesso!'

	def get_success_url(self):
		return reverse('justificativas:tipo_justificativa')


def tipo_justificativa_remove(request, pk):

	tipo_justificativa = get_object_or_404(TipoJustificativaFalta, pk=pk)
	tipo_justificativa.delete()
	messages.success(request, 'Tipo de justificativa de falta excluído com sucesso!')
	return redirect('justificativas:tipo_justificativa')


#Justificativa de falta
class JustificativaListView(ListView):

	model = JustificativaFalta
	template_name = 'justificativas/justificativas.html'

	def get_context_data(self, **kwargs):
		context = super(JustificativaListView, self).get_context_data(**kwargs)
		justificativas = JustificativaFalta.objects

		user = self.request.user

		if(user.is_superuser or user.is_gestor):			
			context['object_list'] = justificativas.all()
		if(user.is_coordenador):						
			#vinculos = user.vinculos.filter(ativo=True, group__name='Coordenador')
			#setores = vinculos.filter(setor__pk__in=vinculos.values('pk'))
			context['object_list'] = justificativas.filter()
		else:		
			context['object_list'] = justificativas.filter(vinculo__user=user)
		return context


class JustificativaCreateView(SuccessMessageMixin, CreateView):

	model = JustificativaFalta
	form_class = EditJustificativaForm
	template_name = 'justificativas/justificativa_create.html'

	success_message = 'Justificativa de falta cadastrado com sucesso!'

	def form_valid(self, form):
		form.save(self.request.user)
		return HttpResponseRedirect(self.get_success_url())

	def get_success_url(self):
		return reverse('justificativas:tipo_justificativa')


#Tipos de justificativa
tipo_justificativa = TipoJustificativaListView.as_view()
tipo_justificativa_create = TipoJustificativaCreateView.as_view()
tipo_justificativa_edit = TipoJustificativaUpdateView.as_view()

#Justificativa de falta
justificativas = JustificativaListView.as_view()
justificativa_create = JustificativaCreateView.as_view()