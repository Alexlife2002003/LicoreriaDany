from django import forms
from .models import UsuariosLicoreria
from django.contrib.auth.models import User


class FormUsuariosLicoreria(forms.ModelForm):
    class Meta:
        model= UsuariosLicoreria
        fields ='__all__'