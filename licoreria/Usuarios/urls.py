from django.contrib.auth.views import LogoutView
from django.urls import path
from Usuarios.views import Login
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('',Login.as_view(),name="login"),

]