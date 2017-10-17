from django.shortcuts import render
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

def index(request):
	return redirect('registro:registro')

def home(request):
	return render(request, 'home.html')