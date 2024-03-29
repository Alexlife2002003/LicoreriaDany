# Generated by Django 4.1.6 on 2023-05-18 22:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('clave', models.AutoField(primary_key=True, serialize=False)),
                ('nombreEmpresa', models.CharField(max_length=100)),
                ('rfc', models.CharField(max_length=13, validators=[django.core.validators.RegexValidator(code='rfc_invalido', message='El RFC no tiene un formato válido', regex='^([A-ZÑ&]{3,4})?(?:- ?)?(\\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\\d|3[01])) ?(?:- ?)?([A-Z\\d]{2})([A\\d])$')], verbose_name='R.F.C.')),
                ('nombreSupervisor', models.CharField(max_length=150)),
                ('diasPedido', models.CharField(choices=[('', '-------------'), ('1', 'Lunes'), ('2', 'Martes'), ('3', 'Miercoles'), ('4', 'Jueves'), ('5', 'Viernes'), ('6', 'Sabado'), ('7', 'Domingo')], max_length=20)),
                ('diasSurtido', models.CharField(choices=[('', '-------------'), ('1', 'Lunes'), ('2', 'Martes'), ('3', 'Miercoles'), ('4', 'Jueves'), ('5', 'Viernes'), ('6', 'Sabado'), ('7', 'Domingo')], max_length=20)),
                ('Descripcion', models.CharField(max_length=200)),
            ],
        ),
    ]
