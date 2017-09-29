from django.urls import reverse
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.views.generic.base import RedirectView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import formset_factory, inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404

from frequencia.vinculos.forms import AdicionarVinculoForm, EditarVinculoForm
from frequencia.vinculos.models import Vinculo

from .models import User
from .forms import RegisterForm, EditAccountForm


class AccountListView(ListView):
	model = User
	template_name = 'accounts/accounts.html'

	def get_queryset(self):
		busca = self.request.GET.get('busca', '')
		return User.objects.buscar(busca) if busca else User.objects.filter(is_active=True)

	def get_context_data(self, **kwargs):
		context = super(AccountListView, self).get_context_data(**kwargs)
		queryset = context['object_list']
		context['busca'] = True if self.request.GET.get('busca') else False
		context['bolsistas'] = queryset.filter(vinculos__ativo=True, vinculos__group__name='Bolsista')
		context['chefes'] = queryset.filter(vinculos__ativo=True, vinculos__group__name='Chefe de setor')
		context['coordenadores'] = queryset.filter(vinculos__ativo=True, vinculos__group__name='Coordenador')
		context['gestores'] = queryset.filter(vinculos__ativo=True, vinculos__group__name='Gestor de unidade')
		return context


def accounts_create(request):
	template_name = 'accounts/accounts_create_edit.html'

	VinculosFormset = formset_factory(AdicionarVinculoForm)
	
	form = RegisterForm(request.POST or None)

	vinculos_form = VinculosFormset(request.POST or None, prefix='vinculos')	

	if form.is_valid() and vinculos_form.is_valid():
		user = form.save()
		for vinculo_form in vinculos_form:			
			vinculo_form.save(user)
		messages.info(request, 'Usuário cadastrado com sucesso!')
		return redirect('accounts:accounts')
	
	context = {
		'form': form,
		'vinculos_formset': vinculos_form,
	}
	return render(request, template_name, context)


def accounts_edit(request, pk): 
	template_name = 'accounts/accounts_create_edit.html'

	instance = get_object_or_404(User, pk=pk)
	form = EditAccountForm(request.POST or None, instance=instance)

	VinculosFormset = inlineformset_factory(User, Vinculo, exclude=('user',), extra=1, can_delete=False, form=EditarVinculoForm)
	vinculos_formset = VinculosFormset(request.POST or None, instance=instance, prefix='vinculos')

	if form.is_valid() and vinculos_formset.is_valid():
		form.save()
		vinculos_formset.save()
		messages.info(request, 'Usuário atualizado com sucesso!')
		return redirect(reverse('accounts:accounts_edit', kwargs={'pk':pk}))
	context = {
		'form': form,
		'vinculos_formset': vinculos_formset,
		'object' : instance,
	}
	return render(request, template_name, context)

@login_required
def edit_password(request):
	template_name = 'accounts/edit_password.html'
	context = {}
	
	form = PasswordChangeForm(data=request.POST or None, user=request.user)
	if form.is_valid():
		form.save()
		messages.info(request, 'Senha alterada com sucesso!')
		#Reautenticando usuário com nova senha		
		update_session_auth_hash(request, form.user)
	
	context['form'] = form
	return render(request, template_name, context)

class ResetPasswordRedirectView(RedirectView):

	permanent = False
	query_string = True

	def get_redirect_url(self, *args, **kwargs):
		user = get_object_or_404(User, pk=kwargs['pk'])
		user.set_password('12345')
		user.save()

		messages.info(self.request, 'Senha do usuário redefinida para <b>12345</b>')
		return reverse('accounts:accounts_edit', kwargs={'pk': user.pk})

accounts = AccountListView.as_view()
reset_password = ResetPasswordRedirectView.as_view()