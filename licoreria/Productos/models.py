from django.db import models
from decimal import Decimal, ROUND_UP
from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    nombre=models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Tipo(models.Model):
    nombre=models.CharField(max_length=100)
    categoria=models.ForeignKey(Categoria, verbose_name="Categoria", on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nombre


Tamanio=[
        ('', '-------------'),
        ('1', '250ml'),
        ('2', '400ml'),
        ('3', '473ml'),
        ('4', '500ml'),
        ('5', '600ml'),
        ('6', '750ml'),
        ('7', '1L'),
        ]

class Producto(models.Model):
    clave = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    tamanio = models.CharField(max_length=10, choices=Tamanio)
    precio = models.DecimalField(max_digits=7, decimal_places=2)
    categoria = models.ForeignKey(Categoria, verbose_name="Categoria", on_delete=models.DO_NOTHING)
    tipo = models.ForeignKey(Tipo, verbose_name="Tipo", on_delete=models.DO_NOTHING)
    existencia=models.PositiveIntegerField()

    @property
    def pricedup(self):
        return round((self.precio * Decimal('1.25')).quantize(Decimal('0.01')))

    def __str__(self):
        return f"{self.nombre}-{self.get_tamanio_display()}-{self.tipo}"


#########################################################

class Venta(models.Model):
    fecha = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.pk}"

class DetalleVenta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE)

    def subtotal(self):
        return self.producto.pricedup * self.cantidad

    def total(self):
        subtotals = DetalleVenta.objects.filter(id_venta=self.id_venta)
        total = sum(detalle.subtotal() for detalle in subtotals)
        rounded_total = Decimal(total).quantize(Decimal('0'), rounding=ROUND_UP)
        return rounded_total


