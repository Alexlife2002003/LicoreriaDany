from django.contrib import admin
from .models import Categoria,Tipo,Producto,Venta

# Register your models here.

admin.site.register(Categoria)
admin.site.register(Tipo)
admin.site.register(Venta)
