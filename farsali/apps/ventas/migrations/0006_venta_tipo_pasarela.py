# Generated by Django 2.2.13 on 2020-11-16 20:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0007_auto_20201116_1738'),
        ('ventas', '0005_auto_20201116_2038'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='tipo_pasarela',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pasarela_set', to='apps.Pasarelas', verbose_name='Pasarela'),
        ),
    ]
