from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import (
    Background,
    Contacto,
    Constante,
    # Farsali,
    GaleriaGeneric,
    Generic,
    Imagen,
    RedSocial,
    Video,
    Pasarelas
)


class ConstanteAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    list_display_links = ('nombre',)
    fieldsets = [
        [_('General'), {
            'fields': (
                'nombre', 'tipo', 'valor',
            )
        }],
        [_('Contenido'), {
            'fields': (
                'enlace_texto',
                'icono_svg',
                'icono',
            )
        }]
    ]
    pass


admin.site.register(Constante, ConstanteAdmin)


class BackgroundAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'titulo',)
    list_display_links = ('codigo', 'titulo',)
    fieldsets = [
        [_('General'), {
            'fields': (
                'codigo', 'video', 'imagen',
                'enlace', ('orden', 'activo',),
            )
        }],
        [_('Contenido'), {
            'fields': (
                'titulo',
                'subtitulo',
            )
        }]
    ]

    pass


admin.site.register(Background, BackgroundAdmin)


class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email',)
    list_display_links = ('nombre',)
    fieldsets = [
        [_('General'), {
            'fields': (
                'nombre', 'email', 'telefono',
                ('orden',),
            )
        }],
        [_('Contenido'), {
            'fields': (
                'contenido',
            )
        }]
    ]
    pass


admin.site.register(Contacto, ContactoAdmin)


class RedSocialAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre',)
    list_display_links = ('codigo', 'nombre',)
    fieldsets = [
        [_('General'), {
            'fields': (
                'codigo', 'tipo', 'url', ('orden',),
            )
        }],
        [_('Contenido'), {
            'fields': (
                'nombre',
                'icono_svg',
                'icono',
            )
        }]
    ]
    pass


admin.site.register(RedSocial, RedSocialAdmin)


class GaleriaGenericAdmin(admin.StackedInline):
    model = GaleriaGeneric
    extra = 1
    pass


class GenericAdmin(admin.ModelAdmin):
    list_display = ('codigo',)
    list_display_links = ('codigo',)
    inlines = [GaleriaGenericAdmin]
    fieldsets = [
        [_('General'), {
            'fields': (
                'codigo', 'enlace', 'imagen', ('orden', 'activo',),
            )
        }],
        [_('Contenido'), {
            'fields': (
                'titulo',
                'subtitulo',
                'descripcion',
            )
        }]
    ]
    pass


admin.site.register(Generic, GenericAdmin)


class ImagenAdmin(admin.ModelAdmin):
    pass


admin.site.register(Imagen, ImagenAdmin)


class VideoAdmin(admin.ModelAdmin):
    pass


admin.site.register(Video, VideoAdmin)


class PasarelasAdmin(admin.ModelAdmin):
    pass


admin.site.register(Pasarelas, PasarelasAdmin)
