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

    def clean(self):
    	cleaned_data = super(FrequenciaForm, self).clean()

    	user = User.objects.filter(cpf=self.cleaned_data['cpf']).first()

    	if not user or not user.is_active or not user.check_password(self.cleaned_data['password']):
    		raise forms.ValidationError("Credenciais inválidas ou usuário inativo")
    	
    	cleaned_data['user'] = user
    	return cleaned_data