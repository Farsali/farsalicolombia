# coding: utf-8
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

# from transmeta import TransMeta


class CategoriaProducto(models.Model):

    # __metaclass__ = TransMeta

    nombre = models.CharField(_(u"Nombre"), max_length=100)
    orden = models.PositiveIntegerField(_(u"Orden"), default=0)
    descripcion = models.TextField(_(u"Descripcion"), blank=True, null=True)
    url = models.SlugField(_(u"Url"), max_length=100)
    imagen = models.ImageField(
        u"Foto categoría",
        upload_to="uploads/inventario/imagenes/",
        default="",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _(u"Categoría Producto")
        verbose_name_plural = _(u"Categorías Productos")
        # translate = ('nombre', 'url', 'descripcion')
        ordering = (
            "orden",
            "id",
        )

    def __unicode__(self):
        return self.nombre

    def __str__(self):
        return self.nombre


class Marca(models.Model):
    """Model definition for Marca."""

    TIPOS_MARCAS = ((0, _(u"Original Farsáli Colombia")), (1, _(u"Marcas Autorizadas")))

    nombre = models.CharField(_(u"Título"), max_length=75)
    descripcion = models.TextField(_(u"Descripcion"), blank=True, null=True)
    tipo_marca = models.SmallIntegerField(_(u"Tipo de Marca"), choices=TIPOS_MARCAS, default=0)
    logo = models.ImageField(
        u"Logo Marca",
        upload_to="uploads/farsali/marcas/",
        default="",
        blank=True,
        null=True,
    )
    activo = models.BooleanField(_(u"Activo"), default=True, db_index=True)
    orden = models.PositiveIntegerField(_(u"Orden"), default=0)

    class Meta:
        """Meta definition for Marca."""

        verbose_name = "Marca"
        verbose_name_plural = "Marcas"
        ordering = ("orden",)

    def __str__(self):
        return self.nombre

    @property
    def get_tipo_marca(self):
        for choice in self.TIPOS_MARCAS:
            if choice[0] == self.tipo_marca:
                return choice[1]
        return ""


class ImagenBase(models.Model):
    nombre = models.CharField(_(u"Nombre"), max_length=100, blank=True, null=False, default="")
    imagen = models.ImageField(
        _(u"Imagen"), upload_to="uploads/inventario/imagenes/", max_length=200
    )
    orden = models.PositiveIntegerField(_(u"Orden"), default=0)
    activo = models.BooleanField(_(u"Activo"), default=True)

    class Meta:
        abstract = True
        ordering = ("orden",)

    @property
    def activa(self):
        return self.activo

    def __unicode__(self):
        return self.nombre


class Producto(models.Model):

    # __metaclass__ = TransMeta

    STAR_QUALITY = (
        (0, _(u"1 estrella")),
        (1, _(u"2 estrella")),
        (2, _(u"3 estrella")),
        (3, _(u"4 estrella")),
        (4, _(u"5 estrella")),
    )

    categoria = models.ForeignKey(
        CategoriaProducto,
        related_name="producto_set",
        verbose_name=_(u"Categoría Producto"),
        on_delete=models.CASCADE,
    )
    codigo = models.CharField(_(u"Referencia"), max_length=39, unique=True)
    url = models.SlugField(_(u"Url"), max_length=100, blank=True, null=True, default="")
    nombre = models.CharField(_(u"Nombre"), max_length=75)
    descripcion = models.TextField(_(u"Descripcion"), blank=True, null=True)
    codigo_video = models.CharField(
        _(u"Código video YouTube"),
        max_length=75,
        blank=True,
        null=True,
    )
    marca_producto = models.ForeignKey(
        Marca,
        related_name="marca_producto",
        verbose_name=_(u"Marca Producto"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    imagen = models.ImageField(
        u"Foto",
        upload_to="uploads/inventario/imagenes/",
        default="",
        blank=True,
        null=True,
    )
    costo = models.FloatField(_(u"Costo"), default=0.0)
    costo_farsali = models.FloatField(_(u"Costo Farsali"), default=0.0)
    activo = models.BooleanField(_(u"Activo"), default=True, db_index=True)
    destacado = models.BooleanField(_(u"Destacado"), default=True, db_index=True)
    calificacion = models.IntegerField(
        _(u"Calificacion"), choices=STAR_QUALITY, blank=True, null=True
    )
    cantidad_cajas = models.PositiveIntegerField(_(u"Cantidad x Cajas"), default=0)
    cantidad_cajas_prefer = models.PositiveIntegerField(_(u"Cantidad x Cajas Farsali"), default=0)
    cantidad = models.PositiveIntegerField(_(u"Cantidad en almacén"))
    orden = models.PositiveIntegerField(_(u"Orden"), default=0)

    descripcion_prefer = models.CharField(
        _(u"Descripcion del producto prefer"), blank=True, null=True, max_length=75
    )
    descripcion_no_prefer = models.CharField(
        _(u"Descripcion del producto no prefer"), blank=True, null=True, max_length=75
    )

    costo_adicional = models.FloatField(_(u"Costo Adicional"), default=0.0)

    descripcion_adicional = models.CharField(
        _(u"Descripcion Adicional del producto"), blank=True, null=True, max_length=75
    )

    by_producto_prefer = models.BooleanField(_(u"Producto Prefer"), default=False)

    class Meta:
        verbose_name = _(u"Producto")
        verbose_name_plural = _(u"Productos")
        # translate = ('nombre', 'url',)
        ordering = ("orden",)

    def __unicode__(self):
        return self.nombre

    def __str__(self):
        return self.nombre

    @property
    def descuento_principal(self):
        try:
            discount = Descuento.objects.filter(
                (Q(categorias_productos_id=self.categoria.id)) | (Q(productos__id=self.id))
            ).first()
            return discount.porcentaje
        except Exception:
            return 0


class GaleriaProducto(ImagenBase, models.Model):
    producto = models.ForeignKey(
        Producto,
        related_name="galeria_producto",
        verbose_name=_(u"Producto"),
        on_delete=models.CASCADE,
    )
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre

    def preview_img(self):
        html = "<div style='display:flex;' >"
        if not self.imagen:
            return mark_safe("<p> No hay imagen para mostrar </p>")
        link = self.imagen.url
        html += (
            '<a target="_blank" href="'
            + link
            + '" ><img style="width:90px;height:90px;border-radius:100px;margin:5px;" src="'
            + link
            + '" /></a>'
        )
        html += "</div>"
        return mark_safe(html)

    preview_img.short_description = "Foto del producto"

    class Meta:
        verbose_name = _(u"Imagen Producto")
        verbose_name_plural = _(u"Galería de Productos")


class Comentario(models.Model):
    """Model definition for Comentario."""

    ESTADOS = (
        (0, _(u"Pendiente de aprobación")),
        (1, _(u"Comentario aprobado")),
        (2, _(u"Comentario denegado")),
    )

    producto = models.ForeignKey(
        Producto,
        related_name="comentario_producto",
        verbose_name=_(u"Producto"),
        on_delete=models.CASCADE,
    )
    ciudad = models.CharField(_(u"Ciudad"), max_length=50, default="", null=True, blank=True)
    estado = models.IntegerField(_(u"Estado"), choices=ESTADOS, default=0)
    comentario = models.TextField(_(u"Comentario"), max_length=1000, default="")
    titulo = models.CharField(_(u"Título"), max_length=150, default="", null=True, blank=True)
    nombre = models.CharField(_(u"Nombre"), max_length=150, default="", null=True, blank=True)
    email = models.EmailField(_(u"Email"), max_length=150, null=True, blank=True)

    localizador = models.CharField(
        _(u"Localizador"), max_length=40, default="", blank=True, null=True
    )

    orden = models.PositiveIntegerField(_(u"Orden"), default=0)
    creado = models.DateTimeField(_(u"Creado"), auto_now_add=True)

    class Meta:
        """Meta definition for Comentario."""

        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
        ordering = ("orden",)

    def __str__(self):
        return self.producto.nombre


class Descuento(models.Model):

    ACTIVO = 1
    INACTIVE = 2

    CONSTANT_STATUS = ((ACTIVO, "Activado"), (INACTIVE, "Desactivado"))

    porcentaje = models.FloatField(
        "Porcentaje del descuento", validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    productos = models.ManyToManyField(
        Producto, verbose_name="Producto", related_name="descuento_productos", blank=True, null=True
    )
    categorias_productos = models.ManyToManyField(
        CategoriaProducto,
        verbose_name="CategoriaProducto",
        related_name="descuento_categorias",
        blank=True,
        null=True,
    )
    nombre = models.CharField(max_length=340)
    estado = models.PositiveSmallIntegerField(choices=CONSTANT_STATUS, default=ACTIVO)
    fecha_expiration = models.DateField(null=True, blank=True)
    prioridad = models.IntegerField("prioridad", default=0)
    creado = models.DateTimeField(_(u"Creado"), auto_now_add=True)
    by_costo = models.BooleanField(_(u"En el costo"), default=False)
    by_costo_caja = models.BooleanField(_(u"En el costo x Caja"), default=False)
    by_costo_mayor = models.BooleanField(_(u"En el costo x Mayor"), default=False)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ("prioridad", "creado")
