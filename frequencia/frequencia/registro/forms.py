from django import forms
from django.core.validators import MaxLengthValidator

from frequencia.accounts.models import User

class FrequenciaForm(forms.Form):

    cpf = forms.CharField(label='CPF', max_length=15)
    observacao = forms.CharField(widget=forms.Textarea, validators=[MaxLengthValidator(200)], max_length=200, required=False)
    password = forms.CharField(widget=forms.PasswordInput)

    widgets = {
            'password': forms.PasswordInput(),
            'observacao': forms.Textarea(),
    }

    def clean(self):
        cleaned_data = super(FrequenciaForm, self).clean()

        if not cleaned_data.get('cpf') or not cleaned_data.get('password'):
            raise forms.ValidationError("Dados de resgistro de frequência inválidos")

        user = User.objects.filter(cpf=self.cleaned_data['cpf']).first()

        if not user or not user.is_active or not user.check_password(self.cleaned_data['password']):
           raise forms.ValidationError("Credenciais inválidas ou usuário inativo")
    
        cleaned_data['user'] = user
        return cleaned_data