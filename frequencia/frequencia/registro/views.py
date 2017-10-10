from rules.contrib.views import PermissionRequiredMixin, permission_required, objectgetter

from django.urls import reverse
from django.contrib import messages
from django.views.generic import ListView
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404, redirect

from frequencia.vinculos.models import Vinculo

from .forms import FrequenciaForm, EditMaquinaForm
from .models import Frequencia, Maquina

import datetime

#Máquinas
class MaquinaListView(PermissionRequiredMixin, ListView):

	model = Maquina
	template_name = 'maquinas/maquinas.html'
	permission_required = 'maquina.can_manage'


class MaquinaCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):

	model = Maquina
	form_class = EditMaquinaForm
	template_name = 'maquinas/maquina_create_edit.html'
	permission_required = 'maquina.can_manage'

	success_message = 'Máquina cadastrada com sucesso!'

	def get_success_url(self):
		return reverse('registro:maquinas')


class MaquinaUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):

	model = Maquina
	form_class = EditMaquinaForm
	template_name = 'maquinas/maquina_create_edit.html'
	permission_required = 'maquina.can_manage'

	success_message = 'Máquina atualizada com sucesso!'

	def get_success_url(self):
		return reverse('registro:maquinas')


@permission_required('maquina.can_manage', fn=objectgetter(Maquina, 'pk'))
def maquina_remove(request, pk):

	maquina = get_object_or_404(Maquina, pk=pk)

	try:
		maquina.delete()
		messages.success(request, 'Máquina excluída com sucesso!')
	except ProtectedError:
		messages.error(request, 'Essa máquina não pode ser removida! Existem registros associados.')
	return redirect('registro:maquinas')


#Registro
def registro(request):

	now = datetime.datetime.now()
	maquina = Maquina.objects.filter(ip=request.META.get('REMOTE_ADDR')).first()

	if not maquina:
		return HttpResponseRedirect(reverse('accounts:login'))

	form = FrequenciaForm(request.POST or None)

	if form.is_valid():
		bolsista = form.cleaned_data['bolsista']
		tipo = 0 if not bolsista.registros_dia() else not bolsista.registros_dia().last().tipo
		frequencia = Frequencia(bolsista=bolsista, maquina=maquina, tipo=tipo, observacao=form.cleaned_data['observacao'])
		frequencia.save()
		
		request.session['bolsista_pk'] = bolsista.pk
		return redirect(reverse('registro:registros_dia'))

	context = {
		'form': form,
		'now':now,
	}

	return render(request, 'registro/registro.html', context)

def registros_dia(request, **kwargs):
	pk = request.session.get('bolsista_pk','')
	bolsista = Vinculo.objects.get(pk=pk) if pk else None

	if not bolsista or not pk:
		return redirect(reverse('registro:registro'))

	request.session['bolsista_pk'] = None
	context = {'bolsista':bolsista}
	return render(request, 'registro/registros_dia.html', context)


#Máquinas
maquinas = MaquinaListView.as_view()
maquina_create = MaquinaCreateView.as_view()
maquina_edit = MaquinaUpdateView.as_view()
