# Generated by Django 3.1.3 on 2020-12-17 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0018_auto_20201217_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='codigo',
            field=models.CharField(max_length=39, unique=True, verbose_name='Referencia'),
        ),
    ]
