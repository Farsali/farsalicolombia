
# coding: utf-8
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.hashers import make_password

from random_username.generate import generate_username


class Cliente(models.Model):

    nombre = models.CharField(
        _(u"Nombre"),
        max_length=100
    )
    email = models.EmailField(
        _(u"Email"),
        max_length=254,
        help_text=_(u'Correo electrónico de contacto')
    )
    contrasena = models.CharField(
        max_length=100
    )
    nick_name = models.CharField(
        _(u'Nombre de usuario'),
        unique=True,
        max_length=100
    )
    cedula = models.CharField(
        _(u'Cédula'),
        unique=True,
        max_length=100
    )
    telefono = models.CharField(
        _(u"Teléfono"),
        max_length=100
    )
    is_farsali = models.BooleanField(
        _(u'Es cliente Farsali'),
        default=False,
        db_index=True
    )
    direccion = models.CharField(
        _(u"Direccion"),
        max_length=100, null=True, blank=True
    )
    locacion = models.CharField(
        _(u'Locación'),
        max_length=100
    )
    # empresa = models.CharField(
    #     _(u'Empresa'),
    #     max_length=100
    # )
    # edad = models.PositiveIntegerField(
    #     _(u'Edad'),
    #     default=0
    # )
    orden = models.PositiveIntegerField(
        _(u'Orden'),
        default=0
    )
    created = models.DateTimeField(
        _(u'Fecha creación'),
        editable=False)
    fecha_activacion = models.DateTimeField(
        _(u'Fecha de activación'),
        blank=True,
        null=True,
        editable=False
    )
    activo = models.BooleanField(_(u'Activo'), default=True)

    class Meta:
        verbose_name = _(u'Cliente')
        verbose_name_plural = _(u'Clientes')
        ordering = ('orden',)

    def __unicode__(self):
        return self.nombre

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.nick_name:
            self.nick_name = generate_username().pop()
        if not self.id:
            self.contrasena = make_password(self.contrasena)
            self.created = timezone.now()
        return super(Cliente, self).save(*args, **kwargs)
