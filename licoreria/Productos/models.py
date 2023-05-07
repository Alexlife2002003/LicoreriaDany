from django.db import models
from decimal import Decimal



class Categoria(models.Model):
    nombre=models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Tipo(models.Model):
    nombre=models.CharField(max_length=100)
    categoria=models.ForeignKey("Productos.Categoria",verbose_name="Categoria", on_delete=models.DO_NOTHING)

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

#Categoria=[
#    ('', '-------------'),
#    ('1', 'Mezcal'),
#    ('2', 'Tequila'),
#    ('3', 'Brandy'),
#    ('4', 'Rompope'),
#    ('5', 'Whisky'),
#    ('6', 'Cerveza'),
#    ('7', 'Bebida Preparada'),
#    ('8', 'Refresco'),
#]

#tipo=[
#    ('', '-------------'),
#    ('2', 'Blanco'),
#    ('3', 'Reposado'),
#    ('4', 'Añejo'),
#    ('5', 'de uva'),
#    ('6', 'de fruta'),
#    ('7', 'de pulpa'),
#    ('8', 'vainilla'),
#    ('9', 'scotch'),
#    ('10', 'Viena'),
#    ('11', 'Pilsner'),
#    ('12', 'Lager'),
#]



class Producto(models.Model):
    clave = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    tamanio = models.CharField(max_length=10, choices=Tamanio)
    precio = models.DecimalField(max_digits=7, decimal_places=2)
    categoria = models.ForeignKey("Productos.Categoria", verbose_name="Categoria", on_delete=models.DO_NOTHING)
    tipo = models.ForeignKey("Productos.Tipo", verbose_name="Tipo", on_delete=models.DO_NOTHING)
    
    
    @property
    def pricedup(self):
        return round((self.precio * Decimal('1.25')).quantize(Decimal('0.01')))

    def __str__(self):
        return f"{self.nombre}-{self.clave}"
