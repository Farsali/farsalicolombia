from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from rangefilter.filter import DateRangeFilter

from .models import Venta, VentaProducts

from weasyprint import HTML
from io import BytesIO
from django.template.loader import get_template
from django.http import HttpResponse
from django.core.files.base import ContentFile
from datetime import datetime
from django.contrib import messages


class VentaProductsAdmin(admin.StackedInline):
    model = VentaProducts
    extra = 0

    readonly_fields = ['producto','cantidad','precio','especificaciones','by_venta_caja']

    fieldsets = [
        [_(u'General'), {
            'fields': (
                'producto',
                ('cantidad', 'precio','by_venta_caja','by_mayor'),
                'especificaciones',
            )
        }]
    ]

    def has_delete_permission(self, request, obj):
        return False

    def has_add_permission(self, request, obj):
        return False

class VentaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cliente',
        'referencia',
        'estado',
        'fecha',
        'tipo_pasarela'
    )
    list_display_links = (
        'id',
    )
    list_filter = (
        'estado',
        ('fecha', DateRangeFilter),
    )
    search_fields = [
        'cliente__nombre',
        'cliente__cedula',
    ]

    readonly_fields = ['fecha','referencia','estado','referencia_pasarela','cliente','tipo_pasarela','total',
                       'cliente_nombre','cliente_farsali','cliente_telefono','cliente_email','cliente_direccion']

    fieldsets = [
        [_(u'General'), {
            'fields': (
                'cliente_nombre',
                'cliente_farsali',
                'cliente_telefono',
                'cliente_email',
                'cliente_direccion',
                'referencia',
                'estado',
                'total',
                'fecha',
                'tipo_pasarela',
                'referencia_pasarela',
                'razon_rechazado'
            )
        }]
    ]

    inlines = (VentaProductsAdmin,)

    actions = ('generate_pdf', 'approved_sale', 'declined_sale')

    def has_add_permission(self, request):
       return False


    def generate_pdf(self, request, queryset):
        item = queryset[0]
        template = get_template("reports/ventas.html")
        products = VentaProducts.objects.filter(venta=item)
        html_template = template.render({
            "reference": item.referencia,
            "date_now":  datetime.now().strftime("%d de %B del %Y"),
            "name_client": item.cliente.nombre,
            "document_client": item.cliente.cedula,
            "address": item.cliente.direccion,
            "location": item.cliente.locacion,
            "phone": item.cliente.telefono,
            "price": "{:,.0f}".format(item.total).replace(',','.'),
            "products": products
        })
        response = BytesIO()
        html = HTML(string=html_template.encode("UTF-8"), base_url=request.build_absolute_uri())
        html.write_pdf(response)
        filename = f'venta_{item.referencia}.pdf'
        response = HttpResponse(ContentFile(response.getvalue()), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    generate_pdf.short_description = "Generar PDF (Sólo 1)"


    def approved_sale(self, request, queryset):
        for item in queryset:
            item.estado = "aprobado"
            item.save()
        self.message_user(request, "Se aprobaron las ventas seleccionados", level=messages.SUCCESS)
        return

    approved_sale.short_description = "Aprobar Venta"

    def declined_sale(self, request, queryset):
        for item in queryset:
            item.estado = "rechazado"
            item.save()
            ventas_productos = VentaProducts.objects.filter(venta=item)
            for item in ventas_productos:
                cantidad = 0
                if item.by_venta_caja:
                    cantidad = item.producto.cantidad_cajas * item.cantidad
                elif item.by_mayor:
                    cantidad = item.producto.cantidad_cajas_prefer * item.cantidad
                else:
                    cantidad = item.cantidad
                item.producto.cantidad -= cantidad
                item.producto.save()
        
        self.message_user(request, "Se rechazaron las ventas seleccionados", level=messages.SUCCESS)
        return
    
    declined_sale.short_description = "Rechazar Venta"

admin.site.register(Venta, VentaAdmin)
