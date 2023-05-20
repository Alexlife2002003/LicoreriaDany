from django.contrib.auth.views import LogoutView
from django.urls import path
from Usuarios.views import Login
from django.contrib.auth.views import LogoutView
from Usuarios import views


urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('',Login.as_view(),name="login"),
    path('lista', views.lista_usuarios, name='lista_usuarios'),
    path('nuevo_usuario',views.crear_usuario,name='nuevo_usuario'),
    path('editar_usuario/<int:pk>',views.editar_usuario,name='editar_usuario'),
    path('eliminar_usuario/<int:pk>',views.EliminarDocentes.as_view(),name='eliminar_usuario'),
    path('asignar-grupos',views.asignar_grupo,name="asignar_grupo"),
    path('remover-grupos/<int:pk>',views.remove_user_groups,name='remover_grupos')
]