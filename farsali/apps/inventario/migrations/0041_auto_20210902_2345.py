# Generated by Django 3.2.6 on 2021-09-02 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0040_auto_20210519_2235'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='by_inactive_price_aditional',
            field=models.BooleanField(default=False, verbose_name='Inactivar precio adicional'),
        ),
        migrations.AddField(
            model_name='producto',
            name='by_inactive_price_farsali',
            field=models.BooleanField(default=False, verbose_name='Inactivar precio Farsali'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='costo_prefer',
            field=models.FloatField(default=0.0, verbose_name='Costo Prefer Caja'),
        ),
    ]
