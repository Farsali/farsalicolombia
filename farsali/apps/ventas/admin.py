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

from farsali.apps.utils import send_invoice
import xlsxwriter


from urllib.request import urlopen


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

    readonly_fields = ['fecha','referencia','estado','referencia_pasarela','cliente','tipo_pasarela','total', 'metodo_pago',
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
                'metodo_pago',
                'referencia_pasarela',
                'razon_rechazado'
            )
        }]
    ]

    inlines = (VentaProductsAdmin,)

    actions = ('generate_pdf', 'approved_sale', 'declined_sale', 'generate_excel')

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

    def generate_excel(self, request, queryset):
        item = queryset[0]

        response = HttpResponse(content_type='application/vnd.ms-excel;charset=utf-8')
        filename = f'venta_{item.referencia}.xls'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        workbook = xlsxwriter.Workbook(response, {'in_memory': True})
        worksheet = workbook.add_worksheet('Factura')
        format1 = workbook.add_format({'border': 0, 'font_size': 10, 'bold': True})
        format2 = workbook.add_format({'border': 0, 'font_size': 10})
        currency_format = workbook.add_format({'border': 0, 'font_size': 10, 'num_format': '$#,##0.00'})

        format3 = workbook.add_format({'border': 0, 'font_size': 10, 'bold': True})
        format3.set_pattern(1)  # This is optional when using a solid fill.
        format3.set_bg_color('#cc98c7')

        currency_format.set_bg_color('#cc98c7')

        worksheet.set_column(1, 1, 25)
        worksheet.set_column(2, 2, 28)
        worksheet.set_column(3, 10, 25)

        worksheet.write('B2', f'Resumen de Compra {item.referencia}', format1)
        worksheet.write('B3', datetime.now().strftime("%d de %B del %Y"), format1)
        worksheet.write('B4', f'{item.cliente.nombre} {item.cliente.cedula}', format1)
        worksheet.write('B5', f'Dirección {item.cliente.direccion}', format1)
        worksheet.write('B5', item.cliente.locacion, format1)
        worksheet.write('B6', f'Teléfono {item.cliente.telefono}', format1)

        url = 'https://farsali-col-bucket.s3.us-east-2.amazonaws.com/img_reports/logo.png'
        image_data = BytesIO(urlopen(url).read())
        
        worksheet.insert_image('D2', url, {'image_data': image_data, 'x_offset': 15, 'y_offset': 10})

        worksheet.write('B9', 'REF', format3)
        worksheet.write('C9', 'CANT', format3)
        worksheet.write('D9', 'PRODUCTO', format3)
        worksheet.write('E9', 'UNIDAD(ES)', format3)
        worksheet.write('F9', 'PRECIO UNITARIO', format3)
        worksheet.write('G9', 'TOTAL', format3)
        worksheet.write('G9', 'ESPECIFICACIONES', format3)

        row = 9
        col = 1

        products = VentaProducts.objects.filter(venta=item)
        for product in products:
            worksheet.write(row, col, product.producto.codigo, format2)
            worksheet.write(row, col + 1, product.cantidad, format2)
            worksheet.write(row, col + 2, product.producto.nombre, format2)

            if product.by_venta_caja:
                worksheet.write(row, col + 3, product.producto.cantidad_cajas, format2)
            else:
                if product.by_mayor:
                    worksheet.write(row, col + 3, product.producto.cantidad_cajas_prefer, format2)
                else:
                    worksheet.write(row, col + 3, "1", format2)
            worksheet.write(row, col + 4, product.precio, format2)
            worksheet.write(row, col + 5, product.cantidad * product.precio, format2)
            worksheet.write(row, col + 6, product.especificaciones, format2)
            row += 1
        
        worksheet.write(row, col, "", format3)
        worksheet.write(row, col + 1, "", format3)
        worksheet.write(row, col + 2, "", format3)
        worksheet.write(row, col + 3, "", format3)
        worksheet.write(row, col + 4, "TOTAl", format3)
        worksheet.write(row, col + 5, item.total, currency_format)

        workbook.close()
        return response

    generate_excel.short_description = "Generar Excel (Sólo 1)"


    def approved_sale(self, request, queryset):
        for item in queryset:
            item.estado = "aprobado"
            item.save()
            
            if item.cliente.email:
                ventas_productos = VentaProducts.objects.filter(venta=item)
                send_invoice(item.cliente.email, item, ventas_productos)
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
