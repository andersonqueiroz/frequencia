from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from frequencia.vinculos.models import Setor

User = get_user_model()

class RegisterForm(forms.ModelForm):

	password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
	password2 = forms.CharField(
		label='Confirmação de Senha', widget=forms.PasswordInput
	)

	groups = forms.ModelChoiceField(
			label='Papéis do usuário',
            queryset=Group.objects.all(),
            )

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Confirmação de senha incorreta")
		return password2

	def save(self, commit=True):
		user = super(RegisterForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password1'])

		if commit:
			user.save()
		return user

	class Meta:
		model = User
		fields = ['name', 'username', 'email', 'cpf', 'is_active']


class EditAccountForm(forms.ModelForm):

	groups = forms.ModelChoiceField(
			label='Papéis do usuário',
            queryset=Group.objects.all(),
            )

	class Meta:
		model = User
		fields = ['username','email','name', 'cpf', 'is_active', 'groups']


