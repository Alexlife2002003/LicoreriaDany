from django import forms
from .models import Proveedor
from django.urls import reverse_lazy

class FormProveedor(forms.ModelForm):
    class Meta:
        model=Proveedor
        fields='__all__'


        widgets = {
            'clave': forms.TextInput(
                attrs={'class':'form-control','placeholder':'Clave Proveedor'}
            ),
            'nombreEmpresa': forms.TextInput(
                attrs={'class':'form-control','placeholder':'Nombre Empresa'}
            ),
            'rfc': forms.TextInput(
                attrs={'class':'form-control','placeholder':'R.F.C'}
            ),
            'nombreSupervisor': forms.TextInput(
                attrs={'class':'form-control','placeholder':'Nombre Empresa'}
            ),
            'diasPedido': forms.Select(
                attrs={'class':'form-control','placeholder':'Dias Pedido'}
            ),
            'diasSurtido': forms.Select(
                attrs={'class':'form-control','placeholder':'Dias Surtido'}
            ),
            'Descripcion': forms.TextInput(
                attrs={'class':'form-control','placeholder':'Descripcion'}
            ),
            
        }


class FiltrosProveedor(FormProveedor):
    
    def __init__(self, *args, **kwargs):
        super(FiltrosProveedor, self).__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].required = False
   