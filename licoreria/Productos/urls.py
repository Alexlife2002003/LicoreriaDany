from django.urls import path, include
from Productos import views

app_name="Producto"
urlpatterns = [
    path('', views.ListaProductos.as_view(), name='lista_productos'),
    path('nuevo',views.NuevoProducto.as_view(),name='nuevo_producto'),
    path('eliminar/<int:clave>', views.eliminar_producto, name='eliminar_producto'),
    path('editar/<int:clave>', views.editar_producto, name='editar_producto'),
    path('editarExistencia/<int:clave>', views.editar_productoExistencia, name='editar_productoExistencia'),
    path('buscar-materia', views.buscar_materia, name='buscar_materia'),
    path('eliminar-productos', views.eliminar_todas,name='eliminar_todas'),
    path('tipos/',views.busca_tipos,name='busca_tipo'),
    path('Venta/', views.create_venta, name='create'),
    path('listVenta/', views.ListaVentas.as_view(), name='list'),
    path('detalle-venta-list',views.ListaDetalleVenta.as_view(),name='detalle_venta_list'),
    path('detalle-venta-create',views.detalle_venta_create,name='detalle_venta_create'),
    path('detalle_venta/<int:id_venta>/', views.detalle_venta_view, name='detalle_venta'),
    path('buscar-venta', views.buscar_detalleventa, name='buscar_venta'),
]