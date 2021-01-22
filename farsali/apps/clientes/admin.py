from django.contrib import admin

from django.utils.translation import ugettext_lazy as _
from .models import Cliente
from rangefilter.filter import DateRangeFilter


class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre',
        'cedula',
        'email',
        'is_farsali',
        'created',
        'fecha_activacion',
    )
    list_display_links = (
        'id',
    )
    list_filter = (
        'is_farsali',
        ('fecha_activacion', DateRangeFilter),
        ('created', DateRangeFilter),
    )
    search_fields = [
        'nombre',
        'email',
    ]

    fieldsets = [
        [_(u'General'), {
            'fields': (
                'nombre',
                'cedula',
                'nick_name',
                'contrasena',
                'email',
                'is_farsali',
                'locacion',
                'telefono',
                'direccion'
            )
        }]
    ]


admin.site.register(Cliente, ClienteAdmin)
