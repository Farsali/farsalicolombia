# coding: utf-8
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail.admin import AdminImageMixin

from .models import CategoriaProducto, Producto, GaleriaProducto, Comentario, Marca
from farsali.forms import ImagenAdminForm


class CategoriaProductoAdmin(admin.ModelAdmin):
    form = ImagenAdminForm

    list_display = (
        'id', 
        'nombre',
        'descripcion',
        'orden',
    )
    list_display_links = (
        'id',
        'nombre', 
    )


    fieldsets = [
        [_(u'General'), {
            'fields': (
                'nombre',
                'descripcion',
                'url',
                'imagen',
                ('orden',),
            )
        }]
    ]


admin.site.register(CategoriaProducto, CategoriaProductoAdmin)


class MarcaAdmin(admin.ModelAdmin):
    form = ImagenAdminForm

    list_display = (
        'id', 
        'nombre',
        'descripcion',
        'tipo_marca',
        'orden',
    )
    list_display_links = (
        'id',
        'nombre', 
    )


    fieldsets = [
        [_(u'General'), {
            'fields': (
                'nombre',
                'descripcion',
                'tipo_marca',
                'logo',
                ('orden','activo'),
            )
        }]
    ]


admin.site.register(Marca, MarcaAdmin)


class GaleriaProductoAdmin(AdminImageMixin, admin.StackedInline):
    form = ImagenAdminForm
    model = GaleriaProducto
    extra = 1

    fieldsets = [
        [_(u'General'), {
            'fields': (
                'nombre',
                'imagen', ('orden', 'activo',),
            )
        }]
    ]


class ProductoAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'nombre',
        'cantidad',
        'codigo',
        'orden',
        'destacado',
        'activo',
    )
    list_display_links = (
        'id',
        'nombre',
    )

    search_fields = (
        'nombre',
        'codigo',
    )

    inlines = (GaleriaProductoAdmin,)

    prepopulated_fields = {}

    fieldsets = [
        [_(u'General'), {
            'fields': (
                'categoria',
                'codigo',
                'costo',
                ('costo_adicional', 'cantidad_cajas'),
                ('costo_farsali','cantidad_cajas_prefer'),
                'cantidad',
                'calificacion',
                'codigo_video',
                'marca_producto',
                'activo',
                'destacado',
                ('orden',),
            )
        }],
        [_(u'Contenido'), {
            'fields': (
                'nombre',
                'url',
                'descripcion',
                'descripcion_adicional',
                'descripcion_no_prefer',
                'descripcion_prefer',
                'imagen',
            )
        }]
    ]

    prepopulated_fields['url'] = ('nombre',)


admin.site.register(Producto, ProductoAdmin)


class ComentarioAdmin(admin.ModelAdmin):
    pass


class ImagenesProductoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre',
        'producto',
        'imagen',
        'orden',
        'activo',
    )
    list_display_links = (
        'id',
        'nombre',
    )

    search_fields = (
        'nombre',
        'producto__nombre',
    )


admin.site.register(Comentario, ComentarioAdmin)
admin.site.register(GaleriaProducto, ImagenesProductoAdmin)
