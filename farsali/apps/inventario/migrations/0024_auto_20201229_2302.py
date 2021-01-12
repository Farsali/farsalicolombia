# Generated by Django 3.1.3 on 2020-12-29 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0023_auto_20201228_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='cantidad_cajas_prefer',
            field=models.PositiveIntegerField(default=0, verbose_name='Cantidad x Cajas Prefer'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='cantidad_cajas',
            field=models.PositiveIntegerField(default=0, verbose_name='Cantidad x Cajas'),
        ),
    ]
