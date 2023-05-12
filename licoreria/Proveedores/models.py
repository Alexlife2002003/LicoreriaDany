from django.db import models
from .validadores import rfc_validador


Dias=[
        ('', '-------------'),
        ('1', 'Lunes'),
        ('2', 'Martes'),
        ('3', 'Miercoles'),
        ('4', 'Jueves'),
        ('5', 'Viernes'),
        ('6', 'Sabado'),
        ('7', 'Domingo'),
        ]

class Proveedor(models.Model):
    clave = models.AutoField(primary_key=True)
    nombreEmpresa = models.CharField(max_length=100)
    rfc = models.CharField('R.F.C.', max_length=13, validators=[rfc_validador])
    nombreSupervisor = models.CharField(max_length=150)
    #diasPedido=models.
    diasPedido =models.CharField(max_length=20, choices=Dias)
    diasSurtido =models.CharField(max_length=20, choices=Dias)
    Descripcion=models.CharField(max_length=200)
    #diasSurtido=

    def __str__ (self):
        return self.nombreEmpresa


