from django.contrib import admin, messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from farsali.apps.ventas.models import Venta


@method_decorator([staff_member_required], name="dispatch")
class ResumenVentasView(TemplateView):
    template_name = "admin/resumen_ventas.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        admin_context = admin.site.each_context(self.request)
        context.update(admin_context)

        result_headers = ["id", "cliente", "referencia", "total", "fecha"]
        result_list = Venta.objects.all().values(
            "id", "cliente__nombre", "referencia", "total", "fecha"
        )
        total = 0
        for item in result_list:
            total += item["total"]

        context.update(
            {
                "title": "Resumen de Ventas",
                "data": result_list,
                "result_headers": result_headers,
                "total": total,
                "cantidades": len(result_list),
            }
        )
        return context
