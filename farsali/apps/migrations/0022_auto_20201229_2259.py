# Generated by Django 3.1.3 on 2020-12-29 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0021_auto_20201203_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='background',
            name='subtitulo',
            field=models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Subtítulo'),
        ),
        migrations.AlterField(
            model_name='background',
            name='titulo',
            field=models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Título'),
        ),
    ]
