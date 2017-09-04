from django import forms


from .models import TipoJustificativaFalta, JustificativaFalta

class EditTipoJustificativaForm(forms.ModelForm):

	class Meta:
		model = TipoJustificativaFalta
		fields = ['nome']


class CreateJustificativaForm(forms.ModelForm):

	class Meta:
		model = JustificativaFalta
		fields = ['tipo', 'descricao', 'inicio', 'termino']

	def save(self, user, commit=True):
		justificativa = super(CreateJustificativaForm, self).save(commit=False)
		vinculos = user.vinculos.filter(ativo=True, group__name='Bolsista')
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

	def save(self, user, commit=True):
		justificativa = super(EditJustificativaForm, self).save(commit=False)
		setor = justificativa.vinculo.setor
		vinculos = user.vinculos.filter(ativo=True, group__name='Chefe de setor', setor=setor)
		if vinculos:
			justificativa.usuario_analise = vinculos.first()
		else:
			raise forms.ValidationError("Usuário não autorizado para homologar justificativa de falta")

		if commit:
			justificativa.save()

		return justificativa