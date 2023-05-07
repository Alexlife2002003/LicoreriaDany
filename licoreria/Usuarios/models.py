from django.db import models
from django.contrib.auth.models import User
from .validadores import rfc_validador,nomapellido_validador


class UsuariosLicoreria(models.Model):
    rfc = models.CharField('R.F.C.', max_length=13, validators=[rfc_validador])
    nombre = models.CharField(max_length=150, validators=[nomapellido_validador]) 
    apellido_paterno = models.CharField(max_length=150,validators=[nomapellido_validador])
    apellido_materno = models.CharField(max_length=150,validators=[nomapellido_validador])
    fecha_nacimiento = models.DateField()
    usuario = models.OneToOneField(User, verbose_name="Usuario", on_delete=models.CASCADE)
