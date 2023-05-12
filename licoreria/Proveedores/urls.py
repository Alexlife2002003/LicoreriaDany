from django.urls import path
from Proveedores import views

urlpatterns =[
    path('',views.ListaProveedores.as_view(),name='lista_proveedores'),
    path('nuevo',views.NuevoProveedor.as_view(),name='nuevo_proveedor'),
    path('editar/<int:clave>', views.editar_proveedor, name='editar_proveedor'),
    path('eliminar/<int:clave>',views.eliminar_proveedor, name='eliminar_proveedor'),
    path('buscar-proveedor', views.buscar_proveedor, name='buscar_proveedor'),
    path('eliminar-proveedores',views.eliminar_todas,name='eliminar_proveedores')

]