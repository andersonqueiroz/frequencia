from rules.contrib.views import PermissionRequiredMixin, permission_required, objectgetter

from django.db.models import Q
from django.urls import reverse
from django.contrib import messages
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404, redirect

from frequencia.vinculos.models import Coordenadoria, Setor
from frequencia.vinculos.utils import get_setores

from .models import TipoJustificativaFalta, JustificativaFalta
from .forms import EditTipoJustificativaForm, CreateJustificativaForm, EditJustificativaForm

#Tipos de justificativa
class TipoJustificativaListView(PermissionRequiredMixin, ListView):

	model = TipoJustificativaFalta
	template_name = 'tipo_justificativa/tipo_justificativa.html'
	permission_required = 'tipo_justificativa.can_manage'


class TipoJustificativaCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):

	model = TipoJustificativaFalta
	form_class = EditTipoJustificativaForm
	template_name = 'tipo_justificativa/tipo_justificativa_create_edit.html'
	permission_required = 'tipo_justificativa.can_manage'

	success_message = 'Tipo de justificativa cadastrado com sucesso!'

	def get_success_url(self):
		return reverse('justificativas:tipo_justificativa')


class TipoJustificativaUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):

	model = TipoJustificativaFalta
	form_class = EditTipoJustificativaForm
	template_name = 'tipo_justificativa/tipo_justificativa_create_edit.html'
	permission_required = 'tipo_justificativa.can_manage'

	success_message = 'Tipo de justificativa atualizado com sucesso!'

	def get_success_url(self):
		return reverse('justificativas:tipo_justificativa')


@permission_required('tipo_justificativa.can_manage', fn=objectgetter(TipoJustificativaFalta, 'pk'))
def tipo_justificativa_remove(request, pk):

	tipo_justificativa = get_object_or_404(TipoJustificativaFalta, pk=pk)
	tipo_justificativa.delete()
	messages.success(request, 'Tipo de justificativa de falta excluído com sucesso!')
	return redirect('justificativas:tipo_justificativa')


#Justificativa de falta
class JustificativaListView(LoginRequiredMixin, ListView):

	model = JustificativaFalta
	template_name = 'justificativas/justificativas.html'

	def get_queryset(self, **kwargs):		

		user = self.request.user

		busca = self.request.GET.get('busca', '')
		justificativas = JustificativaFalta.objects.buscar(busca).order_by('vinculo__setor__pk')

		if not busca:
			justificativas = justificativas.filter(status=0)

		if user.has_perm('accounts.is_gestor'):
			return justificativas.all()			

		if user.has_perm('accounts.is_coordenador_chefe'):
			setores = get_setores(user)
			return justificativas.filter(vinculo__setor__in=setores)
		
		return justificativas.filter(vinculo__user=user)

class JustificativaCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):

	model = JustificativaFalta
	form_class = CreateJustificativaForm
	template_name = 'justificativas/justificativa_create.html'
	permission_required = 'justificativa.can_create'

	success_message = 'Justificativa de falta cadastrada com sucesso!'

	def form_valid(self, form):
		form.save(self.request.user)
		messages.success(self.request, self.success_message)		
		return HttpResponseRedirect(self.get_success_url())

	def get_success_url(self):
		return reverse('justificativas:justificativas')


class JustificativaUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):

	model = JustificativaFalta
	form_class = EditJustificativaForm
	template_name = 'justificativas/justificativa_detail.html'
	permission_required = 'justificativa.can_view'

	success_message = 'Justificativa de falta homologada com sucesso'

	def form_valid(self, form):
		user = self.request.user
		if user.has_perm('justificativa.can_analyse', self.object):
			form.save(self.request.user)
			messages.success(self.request, self.success_message)
			return HttpResponseRedirect(self.get_success_url())
		else:
			raise PermissionDenied()

	def get_success_url(self):
		return reverse('justificativas:justificativa_edit', kwargs={'pk' : self.object.pk})

	def get_context_data(self, **kwargs):
		context = super(JustificativaUpdateView, self).get_context_data(**kwargs)
		context['numero_dias_falta'] = abs((self.object.inicio - self.object.termino).days) + 1
		return context

#Tipos de justificativa
tipo_justificativa = TipoJustificativaListView.as_view()
tipo_justificativa_create = TipoJustificativaCreateView.as_view()
tipo_justificativa_edit = TipoJustificativaUpdateView.as_view()

#Justificativa de falta
justificativas = JustificativaListView.as_view()
justificativa_create = JustificativaCreateView.as_view()
justificativa_edit = JustificativaUpdateView.as_view()
