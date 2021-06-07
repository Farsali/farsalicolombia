# coding: utf-8
import uuid

from django.db import IntegrityError, models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from farsali.apps.clientes.models import Cliente
from farsali.apps.inventario.models import Producto
from farsali.apps.models import Pasarelas
from farsali.apps.utils import generate_random_chars


class Venta(models.Model):
    TIPOS_ESTADO = (
        ('proceso', _(u'Proceso')),
        ('aprobado', _(u'Aprobado')),
        ('pendiente_efectivo', _(u'Pendiente Pago Efectivo')),
        ('rechazado', _(u'Rechazado')),
        ('espera_respuesta_pasarela', _(u'Respuesta de Pasarela')),
        ('error_pasarela', _(u'Error en la Pasarela')),
    )

    uuid = models.UUIDField("UUID", unique=True, default=uuid.uuid4, editable=False, db_index=True)
    cliente = models.ForeignKey(
        Cliente,
        related_name='ventas_set',
        verbose_name=_(u'Cliente'),
        on_delete=models.CASCADE
    )
    referencia = models.CharField(
        _(u'Referencia'),
        editable=False,
        max_length=150,
        unique=True
    )
    referencia_pasarela = models.CharField(
        _(u'Referencia de la Pasarela'),
        max_length=150,
        default="",
        blank=True,
        null=True
    )
    tipo_pasarela = models.ForeignKey(
        Pasarelas,
        related_name='pasarela_set',
        verbose_name=_(u'Pasarela'),
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    fecha = models.DateField(
        _(u'Fecha compra'),
        editable=False)

    total = models.PositiveIntegerField(_(u'Total'), default=0)
    transaccion_id = models.CharField(
        _(u'Transaccion de la Pasarela'),
        max_length=150,
        default="",
        blank=True,
        null=True
    )
    metodo_pago = models.CharField(
        _(u'Metodo de Pago'),
        max_length=150,
        default="",
        blank=True,
        null=True
    )
    estado = models.CharField(_(u'Estado'), max_length=45, choices=TIPOS_ESTADO, default='proceso')
    razon_rechazado = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _(u"Venta")
        verbose_name_plural = _(u"Ventas")
        # translate = ('nombre', 'url',)

    def __str__(self):
        return "{}".format(self.referencia)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps and code '''
        if not self.id:
            self.fecha = timezone.now()
            for count in range(100):
                try:
                    transaction_code = generate_random_chars(6)
                    self.referencia = transaction_code
                    break
                except IntegrityError as e:
                    if 'unique constraint' in e.message and count < 100:
                        pass
                    else:
                        raise e
        return super(Venta, self).save(*args, **kwargs)

    @property
    def cliente_nombre(self):
        return f'{self.cliente.nombre}'

    @property
    def cliente_telefono(self):
        return f'{self.cliente.telefono}'

    @property
    def cliente_email(self):
        return f'{self.cliente.email}'

    @property
    def cliente_direccion(self):
        return f'{self.cliente.direccion} {self.cliente.locacion}'

    @property
    def cliente_farsali(self):
        client_farsali_text = "Si" if self.cliente.is_farsali else "No"
        return f'{client_farsali_text}'

class VentaProducts(models.Model):

    venta = models.ForeignKey(
        Venta,
        related_name='venta_producto',
        verbose_name=_(u'Venta del Producto'),
        on_delete=models.CASCADE
    )
    producto = models.ForeignKey(
        Producto,
        related_name='producto_venta',
        verbose_name=_(u'Productos de la Venta'),
        on_delete=models.CASCADE
    )
    by_venta_caja = models.BooleanField(
        _(u'Cantidad de Caja'),
        default=False
    )
    by_mayor = models.BooleanField(
        _(u'Cantidad x Mayor'),
        default=False
    )
    cantidad = models.PositiveIntegerField(_(u'Cantidad'), default=0)
    precio = models.PositiveIntegerField(_(u'Precio'), default=0)
    especificaciones = models.CharField(
        _(u'Especificaciones del producto'),
        max_length=150,
        default="",
        blank=True,
        null=True
    )

    def __str__(self): 
        return self.producto.nombre
