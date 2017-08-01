from django.shortcuts import render
from django.core.exceptions import PermissionDenied

from frequencia.accounts.models import User

from .forms import FrequenciaForm
from .models import Frequencia, Maquina

import datetime

def registro(request):

	now = datetime.datetime.now()
	maquina = Maquina.objects.filter(ip=request.META.get('REMOTE_ADDR')).first()

	if not maquina:
		raise PermissionDenied

	form = FrequenciaForm(request.POST or None)
	if form.is_valid():	
		user = form.cleaned_data['user']
		tipo = 0 if user.ultima_frequencia_dia == None else not user.ultima_frequencia_dia.tipo
		frequencia = Frequencia(user=user, maquina=maquina, tipo=tipo, observacao=form.cleaned_data['observacao'])
		frequencia.save()
			
	context = {
		'form': form,
		'landing_page': True,
		'now':now,
	}
	return render(request, 'registro/registro.html', context)

	

	
