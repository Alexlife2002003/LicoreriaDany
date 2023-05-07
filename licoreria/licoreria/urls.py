from django.contrib import admin
from django.urls import path,include
from Productos.views import Bienvenido


urlpatterns = [
    path('admin/', admin.site.urls),
    path('bienvenido/',Bienvenido.as_view(),name='bienvenida'),
    path('productos/', include('Productos.urls')),
    path('',include('Usuarios.urls'))
    
]




