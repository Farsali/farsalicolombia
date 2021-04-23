# Generated by Django 3.1.3 on 2021-04-23 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0033_auto_20210412_1746'),
    ]

    operations = [
        migrations.AddField(
            model_name='descuento',
            name='by_costo',
            field=models.BooleanField(default=False, verbose_name='En el costo'),
        ),
        migrations.AddField(
            model_name='descuento',
            name='by_costo_caja',
            field=models.BooleanField(default=False, verbose_name='En el costo x Caja'),
        ),
        migrations.AddField(
            model_name='descuento',
            name='by_costo_mayor',
            field=models.BooleanField(default=False, verbose_name='En el costo x Mayor'),
        ),
    ]
