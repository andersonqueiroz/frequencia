from django import forms
from django.core.validators import MaxLengthValidator

from frequencia.accounts.models import User
from frequencia.vinculos.models import Vinculo

class FrequenciaForm(forms.Form):

    cpf = forms.CharField(label='CPF', max_length=15)
    observacao = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), validators=[MaxLengthValidator(200)], max_length=200, required=False)
    password = forms.CharField(widget=forms.PasswordInput)

    widgets = {
            'password': forms.PasswordInput(),            
    }

    def clean(self):
        cleaned_data = super(FrequenciaForm, self).clean()

        if not cleaned_data.get('cpf') or not cleaned_data.get('password'):
            raise forms.ValidationError("Dados de resgistro de frequência inválidos")

        bolsista = Vinculo.objects.filter(user__cpf=self.cleaned_data['cpf'], ativo=True, user__is_active=True).first()

        if not bolsista or not bolsista.user.check_password(self.cleaned_data['password']):
           raise forms.ValidationError("Credenciais inválidas ou usuário inativo")
    
        cleaned_data['bolsista'] = bolsista
        return cleaned_data