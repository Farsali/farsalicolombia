# Generated by Django 3.1.3 on 2020-12-27 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0021_producto_costo_adicional'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='descripcion_adicional',
            field=models.FloatField(default=0.0, verbose_name='Descripcion Adicional'),
        ),
    ]
