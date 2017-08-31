from django.urls import reverse
from django.db.models import Q, F
from django.contrib import messages
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView

from frequencia.vinculos.models import Coordenadoria, Setor

from .models import TipoJustificativaFalta, JustificativaFalta
from .forms import EditTipoJustificativaForm, CreateJustificativaForm, EditJustificativaForm

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
			return context

		if(user.is_coordenador or user.is_chefe):
			vinculos = user.vinculos.filter(ativo=True)		
			vinculos = vinculos.filter(Q(group__name='Coordenador') | Q(group__name='Chefe de setor'))

			coordenadorias = Coordenadoria.objects.filter(vinculos__in=vinculos)
			setores = Setor.objects.filter(Q(coordenadoria__in=coordenadorias) | Q(vinculos__in=vinculos))

			context['object_list'] = justificativas.filter(vinculo__setor__in=setores)
		else:		
			context['object_list'] = justificativas.filter(vinculo__user=user)
		
		return context

class JustificativaCreateView(SuccessMessageMixin, CreateView):

	model = JustificativaFalta
	form_class = CreateJustificativaForm
	template_name = 'justificativas/justificativa_create.html'

	success_message = 'Justificativa de falta cadastrado com sucesso!'

	def form_valid(self, form):
		form.save(self.request.user)
		return HttpResponseRedirect(self.get_success_url())

	def get_success_url(self):
		return reverse('justificativas:justificativas')


class JustificativaDetailView(DetailView):

	model = JustificativaFalta
	template_name = 'justificativas/justificativa_detail.html'

	def get_object(self):
		justificativa = super(JustificativaDetailView, self).get_object()
		user = self.request.user

		if user.is_superuser or user.is_gestor:
			return justificativa
		
		coordenadorias_user = Coordenadoria.objects.filter(vinculos__user=user)
		user_setores = Setor.objects.filter(Q(vinculos__user=user) | Q(coordenadoria__in=coordenadorias_user))

		if(justificativa.vinculo.setor in user_setores):
			return justificativa
		else:
			raise PermissionDenied

class JustificativaUpdateView(SuccessMessageMixin, UpdateView):

	model = JustificativaFalta
	template_name = 'justificativas/justificativa_detail.html'
	form_class = EditJustificativaForm

	def get_success_url(self):
		return reverse('justificativas:justificativa_edit', kwargs={'pk':self.object.pk})

#Tipos de justificativa
tipo_justificativa = TipoJustificativaListView.as_view()
tipo_justificativa_create = TipoJustificativaCreateView.as_view()
tipo_justificativa_edit = TipoJustificativaUpdateView.as_view()

#Justificativa de falta
justificativas = JustificativaListView.as_view()
justificativa_create = JustificativaCreateView.as_view()
justificativa_details = JustificativaDetailView.as_view()
justificativa_edit = JustificativaUpdateView.as_view()