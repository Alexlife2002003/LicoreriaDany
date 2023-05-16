from django import forms
from .models import Producto
from django.urls import reverse_lazy
from .models import Venta



class FormExistencia(forms.Form):
    existencia = forms.DecimalField(max_digits=5, decimal_places=0, label='Existencia')

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
                attrs={'class':'form-control','placeholder':'Precio Bodega'}
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

######################Venta
class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['producto', 'cantidad']
