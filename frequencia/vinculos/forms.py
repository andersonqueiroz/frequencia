from django import forms
from django.contrib.auth.models import Group

from frequencia.accounts.models import User

from .models import Setor, Coordenadoria, Vinculo

class AdicionarVinculoForm(forms.ModelForm):

	class Meta:
		model = Vinculo
		fields = ['group', 'setor', 'coordenadoria', 'carga_horaria_diaria', 'inicio_vigencia', 'termino_vigencia', 'turno']

	def __init__(self, *args, **kwargs):
		super(AdicionarVinculoForm, self).__init__(*args, **kwargs)
		self.fields['setor'].empty_label = ""
		self.fields['group'].empty_label = None
		self.fields['coordenadoria'].empty_label = ""
		self.fields['inicio_vigencia'].widget = forms.TextInput(attrs={'data-toggle':'datepicker'})
		self.fields['termino_vigencia'].widget = forms.TextInput(attrs={'data-toggle':'datepicker'})

	def clean(self):
		cleaned_data = super(AdicionarVinculoForm, self).clean()
		grupo = cleaned_data.get("group")
		carga_horaria_diaria = cleaned_data.get("carga_horaria_diaria")

		if grupo == 'Bolsista' and not carga_horaria_diaria:
			raise forms.ValidationError("Informe a carga horária diária do bolsista")

		return cleaned_data

	def save(self, user, commit=True):
		vinculo = super(AdicionarVinculoForm, self).save(commit=False)
		vinculo.user = user

		if commit:
			vinculo.save()
		return vinculo

class EditarVinculoForm(forms.ModelForm):

	class Meta:
		model = Vinculo
		fields = ['ativo', 'group', 'setor', 'coordenadoria', 'carga_horaria_diaria', 'inicio_vigencia', 'termino_vigencia', 'turno']

	def __init__(self, *args, **kwargs):
		super(EditarVinculoForm, self).__init__(*args, **kwargs)
		self.fields['setor'].empty_label = ""
		self.fields['group'].empty_label = ""
		self.fields['coordenadoria'].empty_label = ""
		self.fields['inicio_vigencia'].widget = forms.TextInput(attrs={'data-toggle':'datepicker'})
		self.fields['termino_vigencia'].widget = forms.TextInput(attrs={'data-toggle':'datepicker'})

	def clean(self):
		cleaned_data = super(EditarVinculoForm, self).clean()
		grupo = cleaned_data.get("group")
		carga_horaria_diaria = cleaned_data.get("carga_horaria_diaria")

		if grupo.name == 'Bolsista' and not carga_horaria_diaria:
			raise forms.ValidationError({"carga_horaria_diaria": ["Informe a carga horária diária do bolsista",]})

		return cleaned_data

class EditSetorForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(EditSetorForm, self).__init__(*args, **kwargs)
		self.fields['coordenadoria'].empty_label = "Selecione a coordenadoria"

	class Meta:
		model = Setor
		fields = ['nome', 'coordenadoria']

class EditCoordenadoriaForm(forms.ModelForm):

	class Meta:
		model = Coordenadoria
		fields = ['nome']