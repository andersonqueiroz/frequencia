from django.shortcuts import render
from django.core.exceptions import PermissionDenied

from frequencia.accounts.models import User

from .forms import FrequenciaForm
from .models import Frequencia, Maquina

import datetime

def registro(request):
	now = datetime.datetime.now()
	context = {
		'form': FrequenciaForm(),
		'registro': True,
		'now':now,
	}
	return render(request, 'registro/registro.html', context)

def registrar_frequencia(request):	

	maquina = Maquina.objects.filter(ip=request.META.get('REMOTE_ADDR')).first()

	if not maquina:
		raise PermissionDenied

	form = FrequenciaForm(request.POST or None)	
	if form.is_valid():	

		user = User.objects.filter(cpf=form.cleaned_data['cpf']).first()
		if user and user.check_password(form.cleaned_data['password']):
			tipo = 0 if user.ultima_frequencia_dia.tipo else 1
			frequencia = Frequencia(user=user, maquina=maquina, tipo=tipo)
			frequencia.save()			
			
	context = {'form':form}
	return render(request, 'registro/registro.html', context)
