from django import forms
from frequencia.accounts.models import User

class FrequenciaForm(forms.ModelForm):
    class Meta:
        password = forms.CharField(widget=forms.PasswordInput)
        model = User
        fields = ['cpf', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }