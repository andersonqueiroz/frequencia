from datetime import timedelta

from django import forms
from django.db.models import Q

from .models import TipoJustificativaFalta, JustificativaFalta

class EditTipoJustificativaForm(forms.ModelForm):

	class Meta:
		model = TipoJustificativaFalta
		fields = ['nome']


class CreateJustificativaForm(forms.ModelForm):

	class Meta:
		model = JustificativaFalta
		fields = ['tipo', 'descricao', 'inicio', 'termino']
		widgets = {
          'descricao': forms.Textarea(attrs={'rows':3}),
        }

	def __init__(self, *args, **kwargs):
		super(CreateJustificativaForm, self).__init__(*args, **kwargs)
		self.fields['tipo'].empty_label = ""

	def save(self, user, commit=True):
		justificativa = super(CreateJustificativaForm, self).save(commit=False)
		vinculos = user.vinculos.filter(ativo=True)
		if vinculos:
			justificativa.vinculo = vinculos.first()
		else:
			raise forms.ValidationError("Usuário não autorizado para cadastrar justificativa de falta")

		if commit:
			justificativa.save()

		return justificativa

class EditJustificativaForm(forms.ModelForm):

	horas_abonadas = forms.DurationField(initial=timedelta())

	class Meta:
		model = JustificativaFalta
		fields = ['status', 'parecer']
		widgets = {
          'parecer': forms.Textarea(attrs={'rows':3}),
        }

	def clean(self):
		cleaned_data = super(EditJustificativaForm, self).clean()
		if not cleaned_data.get('status'):
			raise forms.ValidationError({'status': ['Status deve ser definido',]})

		return cleaned_data

	def save(self, user, commit=True):
		justificativa = super(EditJustificativaForm, self).save(commit=False)
		setor = justificativa.vinculo.setor
		vinculos = user.vinculos.filter(ativo=True)
		vinculos = user.vinculos.filter(Q(setor=setor) | Q(coordenadoria=setor.coordenadoria))

		if vinculos:
			justificativa.usuario_analise = vinculos.first()
		else:
			raise forms.ValidationError("Usuário não autorizado para homologar justificativa de falta")

		if commit:
			justificativa.save()

		return justificativa