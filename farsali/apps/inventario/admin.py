# coding: utf-8
import sys

from django.contrib import admin, messages
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _
from farsali.apps.task.tasks import send_email_pdf_products
from farsali.forms import ImagenAdminForm
from sorl.thumbnail.admin import AdminImageMixin

from .models import CategoriaProducto, Comentario, Descuento, GaleriaProducto, Marca, Producto


class CategoriaProductoAdmin(admin.ModelAdmin):
    form = ImagenAdminForm

    list_display = (
        "id",
        "nombre",
        "descripcion",
        "orden",
    )
    list_display_links = (
        "id",
        "nombre",
    )

    fieldsets = [
        [
            _("General"),
            {
                "fields": (
                    "nombre",
                    "descripcion",
                    "url",
                    "imagen",
                    ("orden",),
                )
            },
        ]
    ]


admin.site.register(CategoriaProducto, CategoriaProductoAdmin)


class MarcaAdmin(admin.ModelAdmin):
    form = ImagenAdminForm

    list_display = (
        "id",
        "nombre",
        "descripcion",
        "tipo_marca",
        "orden",
    )
    list_display_links = (
        "id",
        "nombre",
    )

    fieldsets = [
        [
            _("General"),
            {
                "fields": (
                    "nombre",
                    "descripcion",
                    "tipo_marca",
                    "logo",
                    ("orden", "activo"),
                )
            },
        ]
    ]


admin.site.register(Marca, MarcaAdmin)


class GaleriaProductoAdmin(AdminImageMixin, admin.StackedInline):
    form = ImagenAdminForm
    model = GaleriaProducto
    extra = 1

    fieldsets = [
        [
            _("General"),
            {
                "fields": (
                    "nombre",
                    "imagen",
                    "enlace",
                    (
                        "orden",
                        "activo",
                    ),
                )
            },
        ]
    ]


class ProductoAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "nombre",
        "cantidad",
        "codigo",
        "orden",
        "destacado",
        "activo",
        "by_producto_prefer",
        "by_producto_prefer_general",
    )
    list_display_links = (
        "id",
        "nombre",
    )

    search_fields = (
        "nombre",
        "codigo",
    )

    inlines = (GaleriaProductoAdmin,)
    list_filter = ("by_producto_prefer",)

    prepopulated_fields = {}

    fieldsets = [
        [
            _("General"),
            {
                "fields": (
                    "categoria",
                    "codigo",
                    "costo",
                    ("costo_adicional", "cantidad_cajas"),
                    ("costo_farsali", "cantidad_cajas_prefer"),
                    "cantidad",
                    "calificacion",
                    "codigo_video",
                    "marca_producto",
                    (
                        "activo",
                        "by_producto_prefer",
                        "by_producto_prefer_general",
                        "by_inactive_price_aditional",
                        "by_inactive_price_farsali",
                    ),
                    "destacado",
                    ("orden",),
                )
            },
        ],
        [
            _("Costos Prefer"),
            {
                "fields": (
                    ("costo_prefer",),
                    ("costo_caja_prefer",),
                )
            },
        ],
        [
            _("Contenido"),
            {
                "fields": (
                    "nombre",
                    "url",
                    "descripcion_adicional",
                    "descripcion_no_prefer",
                    "descripcion_prefer",
                    "descripcion",
                    "imagen",
                )
            },
        ],
    ]

    prepopulated_fields["url"] = ("nombre",)


admin.site.register(Producto, ProductoAdmin)


class ComentarioAdmin(admin.ModelAdmin):
    pass


class ImagenesProductoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "producto",
        "preview_img",
        "orden",
        "activo",
    )
    list_display_links = (
        "id",
        "nombre",
    )

    search_fields = (
        "nombre",
        "producto__nombre",
        "producto__codigo",
    )
    list_filter = ("producto__categoria",)
    readonly_fields = ("preview_img",)

    actions = ("generate_pdf",)
    list_per_page = sys.maxsize

    def generate_pdf(self, request, queryset):
        products_ids = list(queryset.values_list("pk", flat=True))
        send_email_pdf_products.delay(products_ids)
        self.message_user(
            request, "Se enviara un correo con el pdf de las imagenes del productos", level=messages.SUCCESS
        )
        return

    generate_pdf.short_description = "Generar PDF de fotos"


admin.site.register(Comentario, ComentarioAdmin)
admin.site.register(GaleriaProducto, ImagenesProductoAdmin)


class DescuentoAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "nombre",
        "porcentaje",
        "estado",
        "prioridad",
    )
    list_display_links = (
        "id",
        "nombre",
    )

    search_fields = (
        "nombre",
        "estado",
    )

    filter_horizontal = ("productos", "categorias_productos")

    fieldsets = [
        [
            _("General"),
            {
                "fields": (
                    "nombre",
                    "estado",
                    "porcentaje",
                    ("prioridad", "fecha_expiration"),
                )
            },
        ],
        [_("Los Costos"), {"fields": (("by_costo", "by_costo_caja", "by_costo_mayor"),)}],
        [_("Productos"), {"fields": ("productos",)}],
        [_("Categorias de los Productos"), {"fields": ("categorias_productos",)}],
    ]


admin.site.register(Descuento, DescuentoAdmin)
