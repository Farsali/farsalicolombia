# Generated by Django 2.2.13 on 2020-10-24 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0003_galeriaproducto'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='codigo_video',
            field=models.CharField(default='', max_length=75, verbose_name='Código video YouTube'),
            preserve_default=False,
        ),
    ]
