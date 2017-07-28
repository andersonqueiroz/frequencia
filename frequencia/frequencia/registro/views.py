from django.shortcuts import render

from frequencia.accounts.models import User

def registro(request):
	return render(request, 'registro/registro.html')

# Create your views here.
def registrar_frequencia(request):
	
	pass
