from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic.edit import UpdateView, CreateView
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import Group

from .models import User
from .forms import RegisterForm, EditAccountForm


class AccountListView(ListView):
	paginate_by = 10
	model = User
	template_name = 'accounts/accounts.html'


class AccountCreateView(SuccessMessageMixin, CreateView):

	model = User
	form_class = RegisterForm
	template_name = 'accounts/accounts_create_edit.html'	
	
	success_message = 'Conta criada com sucesso!'

	def get_success_url(self):
		return reverse('accounts:accounts_edit', kwargs={'pk':self.object.id})


class AccountUpdateView(SuccessMessageMixin, UpdateView):

	model = User
	form_class = EditAccountForm
	template_name = 'accounts/accounts_create_edit.html'	
	
	success_message = 'Conta <b>%(username)s</b> atualizado com sucesso!'

	def get_success_url(self):
		return reverse('accounts:accounts_edit', kwargs={'pk':self.object.id})


class Login(LoginView):
	template_name = 'accounts/login.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['landing_page'] = True
		return context


@login_required
def edit_password(request):
	template_name = 'accounts/edit_password.html'
	context = {}
	if request.method == 'POST':
		form = PasswordChangeForm(data=request.POST, user=request.user)
		if form.is_valid():
			form.save()
			messages.success(request, 'Senha alterada com sucesso!')
			context['success'] = True
	else:
		form = PasswordChangeForm(user=request.user)
	context['form'] = form
	return render(request, template_name, context)

	

accounts = AccountListView.as_view()
accounts_create = AccountCreateView.as_view()
accounts_edit = AccountUpdateView.as_view()
login = Login.as_view()