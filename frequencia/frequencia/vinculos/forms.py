from django import forms
from .models import Setor, Coordenadoria

class EditSetorForm(forms.ModelForm):

	class Meta:
		model = Setor
		fields = ['nome', 'chefes', 'coordenadoria',]

class EditCoordenadoriaForm(forms.ModelForm):

	class Meta:
		model = Coordenadoria
		fields = ['nome', 'coordenadores',]