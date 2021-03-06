import re

from django import forms
from django.db.models import Q
from django.conf import settings
from django.core.validators import MaxLengthValidator

from .models import TipoJustificativaFalta, JustificativaFalta

class EditTipoJustificativaForm(forms.ModelForm):

	class Meta:
		model = TipoJustificativaFalta
		fields = ['nome', 'comprovante_obrigatorio']


class CreateJustificativaForm(forms.ModelForm):

	class Meta:
		model = JustificativaFalta
		fields = ['tipo', 'descricao', 'inicio', 'termino', 'comprovante']
		widgets = {
          'descricao': forms.Textarea(attrs={'rows':3, 'maxlength':2000}),
        }

	def __init__(self, *args, **kwargs):
		super(CreateJustificativaForm, self).__init__(*args, **kwargs)
		self.fields['tipo'].empty_label = ""
		self.fields['descricao'].validators = [MaxLengthValidator(2000)]		

	def clean_comprovante(self):
		comprovante = self.cleaned_data.get('comprovante', False)	
		max_upload_size = settings.MAX_UPLOAD_SIZE

		if comprovante and comprovante.size > max_upload_size:
			raise forms.ValidationError(['O tamanho do arquivo excede o limite máximo de 5MB.',])

		return comprovante

	def clean(self):
		cleaned_data = super(CreateJustificativaForm, self).clean()
		data_inicio = cleaned_data.get("inicio", '')
		data_termino = cleaned_data.get("termino", '')

		if data_inicio > data_termino:
			raise forms.ValidationError("Data de término deve ser posterior à data de inicio")

		tipo = cleaned_data.get("tipo", '')
		comprovante = self.cleaned_data.get('comprovante', False)
		if tipo.comprovante_obrigatorio and not comprovante:
			raise forms.ValidationError("Este tipo de justificativa exige o cadastro do comprovante de ausência")

		return cleaned_data

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

	class Meta:
		model = JustificativaFalta
		fields = ['status', 'parecer', 'horas_abonadas']
		widgets = {
			'parecer': forms.Textarea(attrs={'rows':3, 'maxlength':2000}),
		}

	def __init__(self, *args, **kwargs):
		super(EditJustificativaForm, self).__init__(*args, **kwargs)		
		self.fields['parecer'].validators = [MaxLengthValidator(2000)]

	def clean_horas_abonadas(self):
		horas = self.data['horas_abonadas']
		pattern = re.compile('^([0-9]){1,2}(:[0-5][0-9]){2}$')

		if horas is None or not pattern.search(str(horas)):
			raise forms.ValidationError(['O tempo abonado deve ser informado no formato HH:MM:SS',])
		return horas

	def clean_status(self):
		if not self.cleaned_data['status']:
			raise forms.ValidationError(['Status deve ser definido',])
		return self.cleaned_data['status']

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
