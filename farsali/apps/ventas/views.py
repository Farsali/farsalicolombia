from django.shortcuts import render
from farsali.apps.ventas.models import Venta


def resumen_ventas(request):
    result_headers = ["id", "cliente", "referencia", "total", "fecha"]
    result_list = Venta.objects.all().values(
        "id", "cliente__nombre", "referencia", "total", "fecha"
    )
    total = 0
    for item in result_list:
        total += item["total"]
    return render(
        request,
        "admin/resumen_ventas.html",
        {
            "data": result_list,
            "result_headers": result_headers,
            "total": total,
            "cantidades": len(result_list),
        },
    )
