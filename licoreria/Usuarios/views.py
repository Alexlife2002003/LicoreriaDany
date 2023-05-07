from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm

class Login(LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm


