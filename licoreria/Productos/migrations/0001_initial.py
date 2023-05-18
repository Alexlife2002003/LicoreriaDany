# Generated by Django 4.1.6 on 2023-05-17 23:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('clave', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('tamanio', models.CharField(choices=[('', '-------------'), ('1', '250ml'), ('2', '400ml'), ('3', '473ml'), ('4', '500ml'), ('5', '600ml'), ('6', '750ml'), ('7', '1L')], max_length=10)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=7)),
                ('existencia', models.DecimalField(decimal_places=0, max_digits=5)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Productos.categoria', verbose_name='Categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('fecha', models.DateField(auto_now_add=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Productos.producto')),
            ],
        ),
        migrations.CreateModel(
            name='Tipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Productos.categoria', verbose_name='Categoria')),
            ],
        ),
        migrations.AddField(
            model_name='producto',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Productos.tipo', verbose_name='Tipo'),
        ),
    ]
