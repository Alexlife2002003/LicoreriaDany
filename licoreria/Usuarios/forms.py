from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class FormUsuariosLicoreria(forms.ModelForm):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class FiltrosUsuario(FormUsuariosLicoreria):
    
    def __init__(self, *args, **kwargs):
        super(FiltrosUsuario, self).__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].required = False