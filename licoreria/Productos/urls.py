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
    path('detalle-venta-list',views.detalle_venta_list,name='detalle_venta_list'),
    path('detalle-venta-create',views.detalle_venta_create,name='detalle_venta_create'),
    path('detalle_venta/<int:id_venta>/', views.detalle_venta_view, name='detalle_venta'),
    #path('eliminarVenta/<int:id>', views.eliminar_venta, name='eliminar_venta'),
    
    # 
    # path('nuevo', views.nueva_materia, name='nueva_materia'),
   # path('eliminar/<str:pk>', views.EliminarMateria.as_view(), name='eliminar_materia'),
    #path('editar/<int:clave>', views.editar_materia, name='editar_materia'),
    #path('editar/<str:pk>', views.EditarMateria.as_view(), name='editar_materia'),
    #path('buscar-materia', views.buscar_materia, name='buscar_materia'),
    #path('eliminar-materias', views.eliminar_todas,name='eliminar_todas')

]