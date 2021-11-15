import ast

import dateutil.parser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from farsali.apps.inventario.models import Producto

# Create your models here.


class Contacto(models.Model):

    nombre = models.CharField(_(u"Nombre"), max_length=100)
    email = models.EmailField(_(u"Email"), max_length=254)
    telefono = models.CharField(_(u"Teléfono"), max_length=50)
    contenido = models.TextField(_(u"Contenido"), blank=True, null=True)
    orden = models.PositiveIntegerField(_(u"Orden"), default=0)

    class Meta:
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"
        ordering = ("orden",)

    def __str__(self):
        return self.nombre


class RedSocial(models.Model):
    TIPO = [
        ["TW", u"Twitter"],
        ["FB", u"Facebook"],
        ["11870", u"11870"],
        ["YTB", u"Youtube"],
        ["GP", u"Google+"],
        ["WP", u"Wordpress"],
        ["FR", u"Flickr"],
        ["PT", u"Pinterest"],
        ["FS", u"Foursquare"],
        ["TA", u"Tripadvisor"],
        ["LI", u"LinkedIn"],
        ["IN", u"Instagram"],
        ["VINE", u"Vine"],
        ["TUM", u"Tumblr"],
        ["VIM", u"Vimeo"],
        ["BL", u"Blog"],
    ]

    nombre = models.CharField(_(u"Nombre"), max_length=100)
    tipo = models.CharField(
        _(u"Tipo"), max_length=10, choices=TIPO, default="TW"
    )
    url = models.URLField(_(u"URL"), max_length=200)
    icono_svg = models.FileField(
        _("Ícono SVG"),
        upload_to="uploads/farsali/red_social/",
        blank=True,
        null=True,
    )
    icono = models.ImageField(
        u"Ícono",
        upload_to="uploads/farsali/red_social/",
        default="",
        blank=True,
        null=True,
    )
    codigo = models.CharField(
        _(u"Código"), max_length=20, blank=True, null=True, default=""
    )
    orden = models.PositiveIntegerField(_(u"Orden"), default=0)

    class Meta:
        verbose_name = _(u"Red social")
        verbose_name_plural = _(u"Redes sociales")
        ordering = ("orden", "pk")

    def __unicode__(self):
        return self.tipo_nombre

    @property
    def tipo_nombre(self):
        u"""
        Devolvemos el nombre del tipo de la red social
        """
        for tipo in self.TIPO:
            if self.tipo == tipo[0]:
                return tipo[1]


class Background(models.Model):
    """Model definition for Background."""

    TIPOS_NAME = (
        ("None", _(u"Ninguno")),
        ("tienda", _(u"Tienda")),
        ("nosotros", _(u"Nosotros")),
        ("home", _(u"Home")),
        ("contacto", _(u"Contacto")),
        ("videos", _(u"Videos")),
        ("politicas", _(u"Politicas")),
        ("videos", _(u"Videos")),
    )

    codigo = models.CharField(
        _(u"Codigo"),
        max_length=45,
        choices=TIPOS_NAME,
        default="None",
        unique=True,
    )
    # codigo = models.CharField(
    #     _(u'Código'),
    #     max_length=100)
    video = models.CharField(
        _(u"Video"), blank=True, null=True, max_length=100
    )
    titulo = models.CharField(
        _(u"Título"), max_length=100, blank=True, null=True, default=""
    )
    subtitulo = models.CharField(
        _(u"Subtítulo"), max_length=100, blank=True, null=True, default=""
    )
    enlace = models.URLField(
        _(u"Enlace"), max_length=200, blank=True, null=True, default=""
    )
    imagen = models.ImageField(
        u"Imagen",
        upload_to="uploads/farsali/backgrounds/",
        default="",
        blank=True,
        null=True,
    )
    activo = models.BooleanField(_(u"Activo"), default=True, db_index=True)
    orden = models.PositiveIntegerField(_(u"Orden"), default=0)

    class Meta:
        """Meta definition for Background."""

        verbose_name = "Imagen Principal"
        verbose_name_plural = "Imágenes Principales"
        ordering = ("orden",)

    def __str__(self):
        titulo = ""
        if self.titulo:
            titulo = self.titulo
        return titulo


class Imagen(models.Model):
    """Model definition for Imagen."""

    # Relación con página (PRÓXIMAMENTE)
    # pagina = models.ForeignKey(OTHERMODEL, on_delete=models.CASCADE)
    enlace = models.URLField(
        _(u"Enlace"), max_length=200, blank=True, null=True, default=""
    )
    codigo = models.CharField(_(u"Código"), max_length=100)
    titulo = models.CharField(_(u"Título"), max_length=75)
    imagen = models.ImageField(
        u"Imagen",
        upload_to="uploads/farsali/imagenes/",
        default="",
        blank=True,
        null=True,
    )
    subtitulo = models.CharField(_(u"Subtítulo"), max_length=100)
    descripcion = models.TextField(
        _(u"Descripcion"), blank=True, null=True
    )
    activo = models.BooleanField(_(u"Activo"), default=True, db_index=True)
    orden = models.PositiveIntegerField(_(u"Orden"), default=0)

    class Meta:
        """Meta definition for Imagen."""

        verbose_name = "Imagen"
        verbose_name_plural = "Imagenes"
        ordering = ("orden",)

    def __str__(self):
        return self.nombre


class Generic(models.Model):
    """Model definition for Generic."""

    # Relación con página (PRÓXIMAMENTE)
    # pagina = models.ForeignKey(OTHERMODEL, on_delete=models.CASCADE)

    codigo = models.CharField(_(u"Código"), max_length=100)
    titulo = models.CharField(_(u"Título"), max_length=75)
    enlace = models.URLField(
        _(u"Enlace"), max_length=200, blank=True, null=True, default=""
    )
    imagen = models.ImageField(
        u"Imagen",
        upload_to="uploads/farsali/imagenes/",
        default="",
        blank=True,
        null=True,
    )
    subtitulo = models.CharField(_(u"Subtítulo"), max_length=100)
    descripcion = models.TextField(
        _(u"Descripcion"), blank=True, null=True
    )
    activo = models.BooleanField(_(u"Activo"), default=True, db_index=True)
    orden = models.PositiveIntegerField(_(u"Orden"), default=0)

    class Meta:
        """Meta definition for Generic."""

        verbose_name = "Generic"
        verbose_name_plural = "Generics"

    def __str__(self):
        return self.titulo


class GaleriaGeneric(models.Model):

    generic = models.ForeignKey(
        Generic,
        related_name="genericgaleria_set",
        verbose_name=_(u"Noticia"),
        on_delete=models.CASCADE,
    )

    nombre = models.CharField(
        _(u"Nombre"), max_length=100, blank=True, null=False, default=""
    )
    imagen = models.ImageField(
        _(u"Imagen"),
        upload_to="uploads/cms_apps/imagenes/",
        max_length=200,
    )
    orden = models.PositiveIntegerField(_(u"Orden"), default=0)
    activo = models.BooleanField(_(u"Activo"), default=True)

    class Meta:
        verbose_name = _(u"Galeria generics")
        verbose_name_plural = _(u"Galería de Generics")
        ordering = ("orden",)

    def __str__(self):
        return self.nombre


class Video(models.Model):
    """Model definition for Video."""

    ORIGEN = ((0, _(u"Youtube")), (1, _(u"Vimeo")))

    titulo = models.CharField(_(u"Título"), max_length=30)
    codigo = models.CharField(_(u"Codigo"), max_length=15)
    imagen = models.ImageField(_(u"Imagen"), upload_to="uploads/videos/")
    origen = models.SmallIntegerField(
        _(u"Origen"), choices=ORIGEN, default=0
    )

    activo = models.BooleanField(_(u"Activo"), default=True)
    orden = models.PositiveIntegerField(_(u"Orden"), default=0)

    class Meta:
        """Meta definition for Video."""

        verbose_name = "Video"
        verbose_name_plural = "Videos"
        ordering = ("orden",)

    def __unicode__(self):
        return "%(titulo)s (%(codigo)s)" % (
            {"titulo": self.titulo, "codigo": self.codigo}
        )


class Pasarelas(models.Model):

    ORIGEN = ((0, _(u"MercadoPago")), (1, _(u"Wompi")), (2, _(u"Epayco")))

    nombre = models.CharField(_(u"Nombre"), max_length=30)
    origen = models.SmallIntegerField(
        _(u"Origen"), choices=ORIGEN, default=0, unique=True
    )
    activo = models.BooleanField(_(u"Activo"), default=False)

    class Meta:
        """Meta definition for Pasarelas."""

        verbose_name = "Pasarela"
        verbose_name_plural = "Pasarelas"

    def __str__(self):
        return self.nombre


class Constante(models.Model):
    u"""
    Modelo para almacenar constantes específicas
    """
    TIPOS_NAME = (
        ("None", _(u"Ninguno")),
        ("contacto_email", _(u"Email")),
        ("contacto_telefono1", _(u"Teléfono")),
        ("contacto_telefono2", _(u"Télefono 2")),
        ("contacto_direccion", _(u"Dirección")),
        ("email_notificacion", _(u"Email Notificacion")),
        ("monto_min", _(u"Monto Mínimo de Compra")),
    )

    TIPOS = (
        ("str", _(u"Cadena")),
        ("int", _(u"Entero")),
        ("list", _(u"Lista")),
        ("dict", _(u"Diccionario")),
        ("bool", _(u"Boleano")),
        ("datetime", _(u"Fecha/Hora")),
    )
    VERDADEROS = frozenset(
        (
            "si",
            "activado",
            "activada",
            "yes",
            "on",
            "true",
            "verdadero",
            "verdadera",
        )
    )

    nombre = models.CharField(
        _(u"Codigo"),
        max_length=45,
        choices=TIPOS_NAME,
        default="None",
        unique=True,
    )

    # nombre = models.CharField(
    #     _(u'Nombre'), max_length=30,
    #     help_text=_(u'En minúsculas. Como si fuera un atributo'))
    enlace_texto = models.CharField(
        _(u"Enlace"),
        max_length=200,
        blank=True,
        null=True,
        help_text=_(
            u"En caso de ser una constante que "
            u"requiera un valor y un enlace externo"
        ),
        default="",
    )
    tipo = models.CharField(
        _(u"Tipo"), max_length=10, choices=TIPOS, default="str"
    )
    valor = models.TextField(_(u"Valor"))
    icono_svg = models.FileField(
        _("Ícono SVG"),
        upload_to="uploads/farsali/constantes/",
        blank=True,
        null=True,
    )
    icono = models.ImageField(
        u"Ícono",
        upload_to="uploads/farsali/constantes/",
        default="",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _(u"Constante")
        verbose_name_plural = _(u"Constantes")

    def __unicode__(self):
        return u"%s-%s" % (self.nombre)

    @property
    def valor_tipo(self):
        u"""
        Devolvemos el valor, pero con el tipo especificado en el modelo. Por
        ejemplo, si la constante es un boleano y como valor tiene un 1,
        devolvemos un True
        """
        if self.tipo == "str":
            return self.valor
        elif self.tipo == "int":
            self.valor = self.valor.replace(" ", "")
            return self.valor
        elif self.tipo in ("list", "dict"):
            return ast.literal_eval(self.valor)
        elif self.tipo == "bool":
            try:
                return bool(int(self.valor))
            except ValueError:
                return self.valor and self.valor.lower() in self.VERDADEROS
        elif self.tipo == "datetime":
            return dateutil.parser.parse(self.valor)
        else:
            return None
