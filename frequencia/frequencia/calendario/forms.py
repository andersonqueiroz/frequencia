from django import forms

from .models import FeriadoCalendarioAcademico

class CreateFeriadoForm(forms.ModelForm):

	class Meta:
		model = FeriadoCalendarioAcademico
		fields = ['nome', 'data']