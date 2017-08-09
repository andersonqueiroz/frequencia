from django import forms
from django.contrib.auth.models import Group

from frequencia.accounts.models import User

from .models import Setor, Coordenadoria, Vinculo

class AdicionarVinculoForm(forms.ModelForm):

	class Meta:
		model = Vinculo
		fields = ['group', 'setor', 'coordenadoria', 'carga_horaria_diaria', 'turno']

	def save(self, user, commit=True):
		vinculo = super(AdicionarVinculoForm, self).save(commit=False)
		vinculo.user = user

		if commit:
			vinculo.save()
		return vinculo

class EditSetorForm(forms.ModelForm):

	class Meta:
		model = Setor
		fields = ['nome', 'coordenadoria']

class EditCoordenadoriaForm(forms.ModelForm):

	class Meta:
		model = Coordenadoria
		fields = ['nome']
