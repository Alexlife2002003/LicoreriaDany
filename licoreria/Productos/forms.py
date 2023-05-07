from django import forms
from .models import Producto
from django.urls import reverse_lazy


class FormProducto(forms.ModelForm):
    class Meta:
        model=Producto
        fields='__all__'

        widgets = {
            'nombre': forms.TextInput(
                attrs={'class':'form-control','placeholder':'Nombre'}
            ),
            'clave': forms.TextInput(
                attrs={'class':'form-control','placeholder':'Clave materia'}
            ),
            'tamanio': forms.Select(
                attrs={'class':'form-control','placeholder':'Tamaño'}
            ),
            #'optativa': forms.CheckboxInput(attrs=()'class':'form-control'),
            'precio': forms.NumberInput(
                attrs={'class':'form-control','placeholder':'precio bodega'}
            ),
            'categoria': forms.Select(
                attrs={'class':'form-control','data-url':reverse_lazy('Producto:busca_tipo')}
            ),
            'tipo': forms.Select(
                attrs={'class':'form-control','placeholder':'tipo'}
            ),
            
        }

class FormProductoEditar(FormProducto):
    class Meta:
        exclude = ['clave']
        model = Producto

class FiltrosProducto(FormProducto):
    
    def __init__(self, *args, **kwargs):
        super(FiltrosProducto, self).__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].required = False