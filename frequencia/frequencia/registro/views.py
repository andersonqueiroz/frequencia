from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView

from .forms import FrequenciaForm
from .models import Frequencia, Maquina

import datetime

def registro(request):

	now = datetime.datetime.now()
	maquina = Maquina.objects.filter(ip=request.META.get('REMOTE_ADDR')).first()

	if not maquina:
		raise PermissionDenied

	form = FrequenciaForm(request.POST or None)

	context = {
		'form': form,
		'landing_page': True,
		'now':now,
	}

	if form.is_valid():	
		bolsista = form.cleaned_data['bolsista']
		tipo = 0 if not bolsista.registros_dia() else not bolsista.registros_dia().last().tipo
		frequencia = Frequencia(bolsista=bolsista, maquina=maquina, tipo=tipo, observacao=form.cleaned_data['observacao'])
		frequencia.save()
		context['bolsista'] = bolsista
		return render(request, 'registro/registros_dia.html', context)
			
	return render(request, 'registro/registro.html', context)
