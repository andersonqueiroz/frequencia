from datetime import date

from django import forms

class NovaMensagemForm(forms.Form):

	texto = forms.CharField(widget=forms.Textarea, max_length=2000)

	def __init__(self, setores, *args, **kwargs):
		super(NovaMensagemForm, self).__init__(*args, **kwargs)

		#Popular listagem de setores		
		self.fields['setores'] = forms.ModelMultipleChoiceField(
									required=True, 
									queryset=setores, 
									label='Setor', 
									help_text='Selecione os setores para o envio da mensagem')