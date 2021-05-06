# Generated by Django 3.1.3 on 2021-04-29 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0035_galeriaproducto_updated_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='galeriaproducto',
            options={'ordering': ('-updated_at',), 'verbose_name': 'Imagen Producto', 'verbose_name_plural': 'Galería de Productos'},
        ),
        migrations.AddField(
            model_name='producto',
            name='by_producto_prefer_general',
            field=models.BooleanField(default=False, verbose_name='Producto Prefer y Generales'),
        ),
    ]