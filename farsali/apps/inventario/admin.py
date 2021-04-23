# coding: utf-8
import random
from io import BytesIO

from django.contrib import admin
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _
from farsali.forms import ImagenAdminForm
from sorl.thumbnail.admin import AdminImageMixin
from weasyprint import HTML

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
                    ("activo", "by_producto_prefer"),
                    "destacado",
                    ("orden",),
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

    def generate_pdf(self, request, queryset):
        template = get_template("reports/imagenes_products.html")
        html_template = template.render({"data_imagenes": list(queryset)})
        response = BytesIO()
        html = HTML(string=html_template.encode("UTF-8"), base_url=request.build_absolute_uri())
        html.write_pdf(response)
        number = random.randrange(100000)
        filename = f"fotos_{number}.pdf"
        response = HttpResponse(ContentFile(response.getvalue()), content_type="application/pdf")
        response["Content-Disposition"] = f"attachment; filename={filename}"
        return response

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
