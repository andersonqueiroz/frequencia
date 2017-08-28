from django import forms

from .models import TipoJustificativaFalta

class EditTipoJustificativaForm(forms.ModelForm):

	class Meta:
		model = TipoJustificativaFalta
		fields = ['nome']