# Generated by Django 2.2.13 on 2020-09-12 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='calificacion',
            field=models.IntegerField(blank=True, choices=[(0, '1 estrella'), (1, '2 estrella'), (2, '3 estrella'), (3, '4 estrella'), (4, '5 estrella')], null=True, verbose_name='Calificacion'),
        ),
    ]
