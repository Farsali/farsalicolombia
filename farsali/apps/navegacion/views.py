# coding: utf-8
import json

import mercadopago
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView
from django.views.generic.base import View
from farsali.apps.clientes.models import Cliente
from farsali.apps.models import Constante
from farsali.apps.utils import send_invoice
from farsali.apps.ventas.models import Venta, VentaProducts
from farsali.settings import (EPAYCO_PUBLIC_KEY, MERCADOPAGO_ACCESS_TOKEN,
                              MERCADOPAGO_URL, WOMPI_PUBLIC_KEY)

from ..inventario.models import (CategoriaProducto, Comentario, Descuento,
                                 Marca, Producto)
from ..models import Background, Generic, Pasarelas


def dict_producto(producto):
    fotos = [
        {
            "nombre": foto.nombre,
            "imagen": {"url": foto.imagen.url if foto.imagen else foto.enlace},
        }
        for foto in producto.galeria_producto.all()
    ]
    if not fotos:
        fotos = [
            {
                "nombre": producto.nombre,
                "imagen": {
                    "url": producto.imagen.url if producto.imagen else foto.enlace,
                },
            }
        ]

    # Comentarios del producto
    comentarios = [
        {
            "nombre_cliente": comentario.nombre,
            "ciudad": comentario.ciudad,
            "comentario": comentario.comentario,
            "titulo": comentario.titulo,
            "fecha": comentario.creado,
        }
        for comentario in producto.comentario_producto.filter(estado=1).order_by("orden", "creado")
    ]

    discount = Descuento.objects.filter(
        (Q(categorias_productos__id=producto.categoria_id)) | (Q(productos__id=producto.id))
    ).first()
    descuento = discount.porcentaje if discount else 0

    descuento_unidad = 0
    descuento_mayor = 0
    descuento_caja = 0
    if discount:
        if discount.by_costo:
            descuento_unidad = producto.costo - (producto.costo * (descuento / 100))

        if discount.by_costo_mayor:
            descuento_mayor = producto.costo_farsali - (producto.costo_farsali * (descuento / 100))

        if discount.by_costo_caja:
            descuento_caja = producto.costo_adicional - (
                producto.costo_adicional * (descuento / 100)
            )

    product_dict = {
        "id": producto.id,
        "nombre": producto.nombre,
        "orden": producto.orden,
        "descripcion": producto.descripcion,
        "descuento_principal": descuento,
        "descuento_unidad": descuento_unidad,
        "descuento_mayor": descuento_mayor,
        "descuento_caja": descuento_caja,
        "descripcion_adicional": producto.descripcion_adicional
        if producto.descripcion_adicional
        else "",
        "descripcion_no_prefer": producto.descripcion_no_prefer
        if producto.descripcion_no_prefer
        else "",
        "descripcion_prefer": producto.descripcion_prefer if producto.descripcion_prefer else "",
        "categoria_id": producto.categoria_id,
        "codigo": producto.codigo,
        "imagen": producto.imagen,
        "cantidad": producto.cantidad,
        "cantidad_cajas_prefer": producto.cantidad_cajas_prefer,
        "calificacion": producto.calificacion,
        "cantidad_cajas": producto.cantidad_cajas,
        "costo_adicional": producto.costo_adicional,
        "costo": producto.costo,
        "costo_farsali": producto.costo_farsali,
        "categoria_url": producto.categoria.url,
        "url_video": producto.codigo_video,
        "fotos": fotos,
        "comentarios": comentarios,
        "by_producto_prefer": producto.by_producto_prefer,
        "by_producto_prefer_general": producto.by_producto_prefer_general,
    }

    return product_dict


def get_productos(**kwargs):
    fields = [
        "id",
        "nombre",
        "descripcion",
        "categoria_id",
        "codigo",
        "imagen",
        "calificacion",
        "costo",
        "cantidad_cajas",
        "by_producto_prefer",
        "by_producto_prefer_general",
    ]
    map_fields = {
        "categoria_url": F("categoria__url"),
    }
    filter_kwargs = {"activo": True, "destacado": False}
    exclude = {}
    if kwargs.get("filter"):
        filter_kwargs.update(kwargs.get("filter"))
    if kwargs.get("exclude"):
        exclude.update(kwargs.get("exclude"))
    # TODO quitarlo en la noche
    productos_qs = Producto.objects.filter(**filter_kwargs).exclude(**exclude)[:40]
    productos = productos_qs.values(*fields, **map_fields)
    for p in productos:
        p["calificacion_cantidad"] = (
            range(0, p["calificacion"] + 1) if p.get("calificacion") else []
        )
    return productos


def get_generics(**kwargs):
    filter_kwargs = {"activo": True}
    if kwargs.get("filter"):
        filter_kwargs.update(kwargs.get("filter"))
    generics = Generic.objects.filter(**filter_kwargs)
    if kwargs.get("exclude"):
        filter_kwargs.update(kwargs.get("exclude"))
    generics = Generic.objects.filter(**filter_kwargs)
    return generics


def get_backgrounds(**kwargs):
    filter_kwargs = {"activo": True}
    if kwargs.get("filter"):
        filter_kwargs.update(kwargs.get("filter"))
    productos_qs = Producto.objects.filter(**filter_kwargs)
    if kwargs.get("exclude"):
        productos_qs.exclude(**kwargs.get("exclude"))
    background = Background.objects.filter(**filter_kwargs).first()
    return background


def get_marcas(**kwargs):
    filter_kwargs = {"activo": True}
    marcas = Marca.objects.filter(**filter_kwargs).order_by("orden")
    return marcas


def productsView(request):
    page_number = request.GET.get("page") if request.GET.get("producto_id") else None
    producto_id = request.GET.get("producto_id") if request.GET.get("producto_id") else None
    marca_id = request.GET.get("marca_id") if request.GET.get("marca_id") else None
    category_id = request.GET.get("category_id") if request.GET.get("category_id") else None
    search_product = (
        request.GET.get("search_product") if request.GET.get("search_product") else None
    )
    producto_prefer = (
        request.GET.get("by_producto_prefer") if request.GET.get("by_producto_prefer") else None
    )

    quantity = 10
    pagination = int(page_number) * quantity
    product = None
    by_producto_prefer = False
    if producto_id and int(producto_id) > 0:
        product = Producto.objects.get(pk=producto_id)

    if producto_prefer and int(producto_prefer) > 0:
        by_producto_prefer = True

    fields = [
        "id",
        "nombre",
        "descripcion",
        "categoria_id",
        "codigo",
        "imagen",
        "calificacion",
        "costo",
        "cantidad",
        "cantidad_cajas_prefer",
        "cantidad_cajas",
        "costo_adicional",
        "costo_farsali",
        "descripcion_prefer",
        "descripcion_adicional",
        "descripcion_no_prefer",
        "costo_prefer",
        "costo_caja_prefer",
    ]
    productos_qs = None
    if product:
        queryset = (
            (Q(by_producto_prefer=by_producto_prefer) | Q(by_producto_prefer_general=True))
            & (Q(activo=True))
            & (Q(orden__gte=product.orden))
            & (Q(cantidad__gt=0) | Q(cantidad_cajas__gt=0) | Q(cantidad_cajas_prefer__gt=0))
        )
        if category_id and int(category_id) > 0:
            queryset = queryset & (Q(categoria_id=category_id))
        if search_product and search_product != "":
            queryset = queryset & (Q(nombre__icontains=search_product))
        productos_qs_gt = (
            Producto.objects.filter(queryset)
            .exclude(id=product.id)
            .order_by("orden", "id")[int(pagination) : int(pagination) + quantity]
        )
        productos_qs_gt = productos_qs_gt.values(*fields)
        productos_qs_lt = []
        if len(productos_qs_gt) < quantity:
            queryset = (
                (Q(by_producto_prefer=by_producto_prefer) | Q(by_producto_prefer_general=True))
                & (Q(activo=True))
                & (Q(orden__lt=product.orden))
                & (Q(cantidad__gt=0) | Q(cantidad_cajas__gt=0) | Q(cantidad_cajas_prefer__gt=0))
            )
            if category_id and int(category_id) > 0:
                queryset = queryset & (Q(categoria_id=category_id))
            if search_product and search_product != "":
                queryset = queryset & (Q(nombre__icontains=search_product))
            productos_qs_lt = (
                Producto.objects.filter(queryset)
                .exclude(id=product.id)
                .order_by("orden", "id")[int(pagination) : int(pagination) + quantity]
            )
            productos_qs_lt = productos_qs_lt.values(*fields)
        productos = list(productos_qs_gt) + list(productos_qs_lt)
    elif marca_id and int(marca_id) > 0:
        marca = Marca.objects.get(pk=marca_id)
        queryset = (
            (Q(by_producto_prefer=by_producto_prefer) | Q(by_producto_prefer_general=True))
            & (Q(activo=True))
            & (Q(marca_producto=marca))
            & (Q(cantidad__gt=0) | Q(cantidad_cajas__gt=0) | Q(cantidad_cajas_prefer__gt=0))
        )
        if category_id and int(category_id) > 0:
            queryset = queryset & (Q(categoria_id=category_id))
        if search_product and search_product != "":
            queryset = queryset & (Q(nombre__icontains=search_product))
        productos_qs = Producto.objects.filter(queryset).order_by("orden", "id")[
            int(pagination) : int(pagination) + quantity
        ]
        productos = productos_qs.values(*fields)
    else:
        queryset = (
            (Q(by_producto_prefer=by_producto_prefer) | Q(by_producto_prefer_general=True))
            & (Q(activo=True))
            & (Q(cantidad__gt=0) | Q(cantidad_cajas__gt=0) | Q(cantidad_cajas_prefer__gt=0))
        )
        if category_id and int(category_id) > 0:
            queryset = queryset & (Q(categoria_id=category_id))
        if search_product and search_product != "":
            queryset = queryset & (Q(nombre__icontains=search_product))
        productos_qs = Producto.objects.filter(queryset).order_by("orden", "id")[
            int(pagination) : int(pagination) + quantity
        ]
        [item.descuento_principal for item in productos_qs]
        productos = productos_qs.values(*fields)

    for p in productos:
        p["imagen"]
        p["calificacion_cantidad"] = (
            list(range(0, p["calificacion"] + 1)) if p.get("calificacion") else []
        )
        discount = Descuento.objects.filter(
            (Q(categorias_productos__id=p["categoria_id"])) | (Q(productos__id=p["id"]))
        ).first()
        if discount:
            descuento = discount.porcentaje
            descuento_unidad = 0
            descuento_mayor = 0
            descuento_caja = 0
            if discount.by_costo:
                descuento_unidad = p["costo"] - (p["costo"] * (descuento / 100))

            if discount.by_costo_mayor:
                descuento_mayor = p["costo_farsali"] - (p["costo_farsali"] * (descuento / 100))

            if discount.by_costo_caja:
                descuento_caja = p["costo_adicional"] - (p["costo_adicional"] * (descuento / 100))

            p["descuento_principal"] = {
                "descuento": discount.porcentaje,
                "descuento_unidad": descuento_unidad,
                "descuento_mayor": descuento_mayor,
                "descuento_caja": descuento_caja,
            }
        else:
            p["descuento_principal"] = {"descuento": 0, "descuento_unidad": 0}

    return JsonResponse({"error": False, "data": list(productos)}, status=200, safe=False)


def categoryView(request):
    category = CategoriaProducto.objects.all().values("id", "nombre", "url")
    return JsonResponse({"error": False, "data": list(category)}, status=200, safe=False)


class homeView(TemplateView):
    template_name = "base/home.html"
    page_name = "home"

    def paginate_highlights(self, context):
        productos_qs = Producto.objects.filter(activo=True)
        user = self.request.session.get("username", None)
        prefer = False
        if user:
            prefer = True
        my_model = productos_qs.filter(destacado=True, by_producto_prefer=prefer)
        number_of_item = 6
        paginatorr = Paginator(my_model, number_of_item)
        first_page = paginatorr.page(1).object_list
        page_range = paginatorr.page_range
        context.update(
            {
                "paginatorr": paginatorr,
                "first_page": first_page,
                "page_range": page_range,
                "marcas": get_marcas(),
                "background": get_backgrounds(
                    filter={"codigo": self.request.resolver_match.url_name}
                ),
            }
        )
        if self.request.method == "POST":
            page_n = self.request.POST.get("page_n", None)
            results = list(paginatorr.page(page_n).object_list)
            return JsonResponse({"results": results})
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        productos_qs = get_productos()
        user = self.request.session.get("username", None)
        prefer = False
        if user:
            prefer = True
        productos_hg = get_productos(
            **{"filter": {"destacado": True, "by_producto_prefer": prefer}}
        )
        categorias_qs = CategoriaProducto.objects.all()
        context.update(
            {
                "page_name": self.page_name,
                "productos": productos_qs,
                "productos_destacados": productos_hg,
                "marcas": get_marcas(),
                "categorias": categorias_qs,
                "background": get_backgrounds(
                    filter={"codigo": self.request.resolver_match.url_name}
                ),
            }
        )
        return context


class contactoView(TemplateView):
    template_name = "base/contacto.html"
    page_name = "contacto"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "page_name": self.page_name,
                "marcas": get_marcas(),
                "background": get_backgrounds(
                    filter={"codigo": self.request.resolver_match.url_name}
                ),
            }
        )
        return context


class marcasView(TemplateView):
    template_name = "base/marcas.html"
    page_name = "marcas"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            marca = Marca.objects.get(pk=self.kwargs["pk"])
        except Marca.DoesNotExist:
            raise Http404("Marca no existe")

        productos_marca = get_productos(**{"filter": {"marca_producto": marca}})
        context.update(
            {
                "page_name": self.page_name,
                "marcas": get_marcas(),
                "marca": marca,
                "marca_id": marca.id,
                "background": get_backgrounds(
                    filter={"codigo": self.request.resolver_match.url_name}
                ),
            }
        )
        return context


class redesView(TemplateView):
    template_name = "base/redes.html"
    page_name = "redes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"page_name": self.page_name})
        return context


class nosotrosView(TemplateView):
    template_name = "base/nosotros.html"
    page_name = "nosotros"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        generics = get_generics(filter={"codigo": self.request.resolver_match.url_name})
        context.update(
            {
                "page_name": self.page_name,
                "generics": generics,
                "marcas": get_marcas(),
                "background": get_backgrounds(
                    filter={"codigo": self.request.resolver_match.url_name}
                ),
            }
        )
        return context


class tiendaView(TemplateView):
    template_name = "base/tienda.html"
    page_name = "tienda"

    def get_context_data(self, **kwargs):
        productos_qs = get_productos()
        productos_hg = get_productos(**{"filter": {"destacado": True}})
        categorias_qs = CategoriaProducto.objects.all()
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "page_name": self.page_name,
                "productos": productos_qs,
                "productos_destacados": productos_hg,
                "categorias": categorias_qs,
                "marcas": get_marcas(),
                "background": get_backgrounds(
                    filter={"codigo": self.request.resolver_match.url_name}
                ),
            }
        )
        return context


class videosView(TemplateView):
    template_name = "base/videos.html"
    page_name = "videos"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        videos = (
            Producto.objects.exclude(codigo_video__isnull=True)
            .exclude(codigo_video__exact="")
            .values("codigo_video", "nombre")
        )
        context.update({"page_name": self.page_name, "marcas": get_marcas(), "videos": videos})
        return context


class politicasView(TemplateView):
    template_name = "base/politicas.html"
    page_name = "politicas"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_code = self.request.resolver_match.url_name
        generics = get_generics(filter={"codigo": page_code})
        context.update(
            {
                "page_name": self.page_name,
                "generics": generics,
                "background": get_backgrounds(filter={"codigo": page_code}),
            }
        )
        return context


class productsDetailView(TemplateView):
    template_name = "base/producto_detalle.html"
    page_name = "Producto Detalle"
    producto = None

    def dispatch(self, request, *args, **kwargs):
        self.producto = get_object_or_404(Producto, pk=kwargs.get("id_producto"))
        return super(productsDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            producto = dict_producto(self.producto)
            user = self.request.session.get("username", None)
            if producto["by_producto_prefer"] == True and not user:
                producto = None
        except Producto.DoesNotExist:
            producto = None

        if not producto:
            raise Http404("Marca no existe")
        productos_hg = get_productos(**{"filter": {"destacado": True}})
        # categorias_qs = CategoriaProducto.objects.all()
        producto["calificacion_cantidad"] = (
            range(0, producto["calificacion"] + 1) if (producto["calificacion"]) else []
        )
        context.update(
            {
                "page_name": self.page_name,
                "producto": producto,
                "marcas": get_marcas(),
                "productos_id": producto["id"],
                "productos_destacados": productos_hg,
                "background": get_backgrounds(
                    filter={"codigo": self.request.resolver_match.url_name}
                ),
            }
        )
        return context


def checkoutView(request):
    items = []
    total = 0
    if request.POST:
        data = None
        validate_buy = None
        if request.POST.get("productos-checkout-detail"):
            data = request.POST.get("productos-checkout-detail")
            validate_buy = request.POST.get("validate-buy")
        elif request.POST.get("productos-checkout"):
            data = request.POST.get("productos-checkout")
        json_data = json.loads(data)
        print(json_data)
        for item in json_data:
            try:
                producto = Producto.objects.get(id=int(item["id"]))
                total += int(item["precio"]) * int(item["cantidad"])
                total += int(item["precio_caja"]) * int(item["cantidad_cajas"])
                total += int(item["precio_xmayor"]) * int(item["cantidad_xmayor"])
                items.append(
                    {
                        "title": producto.nombre,
                        "description_aditional": producto.descripcion_adicional,
                        "description_prefer": producto.descripcion_prefer,
                        "description_no_prefer": producto.descripcion_no_prefer,
                        "quantity": int(item["cantidad"]),
                        "quantity_box": int(item["cantidad_cajas"]),
                        "unit_price_box": int(item["precio_caja"]),
                        "quantity_xmayor": int(item["cantidad_xmayor"]),
                        "unit_price_xmayor": int(item["precio_xmayor"]),
                        "currency_id": "COP",
                        "unit_price": int(item["precio"]),
                        "specs": item["especificaciones"],
                        "id": int(item["id"]),
                    }
                )
            except ObjectDoesNotExist:
                pass
    return render(
        request,
        "base/checkout.html",
        context={
            "page_name": "Compra",
            "products": items,
            "total": total,
            "validate_buy": validate_buy,
        },
    )


def paymentClienteView(request):
    page_name = "Datos del Cliente"
    json_data = []
    if request.POST:
        data = None
        if request.POST.get("productos-payment-1"):
            data = request.POST.get("productos-payment-1")
        elif request.POST.get("productos-payment-2"):
            data = request.POST.get("productos-payment-2")
        json_data = json.loads(data)
        print(json_data)
    return render(
        request, "base/payment_client.html", context={"page_name": page_name, "products": json_data}
    )


class redirectPaymentView(View):
    page_name = "Confirmacion de Pago"

    def get(self, request, *args, **kwargs):
        venta_id = self.kwargs["reference"]
        success = request.GET.get("success") if request.GET.get("success") else None
        failure = request.GET.get("failure") if request.GET.get("failure") else None
        venta = Venta.objects.get(pk=venta_id)
        ventas_productos = None
        if venta.tipo_pasarela.origen == 0:
            if success:
                if venta.estado == "proceso":
                    ventas_productos = VentaProducts.objects.filter(venta=venta)
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
                if venta.cliente.email:
                    send_invoice(venta.cliente.email, venta, ventas_productos)
                venta.estado = "aprobado"
            elif failure:
                if venta.estado == "espera_respuesta_pasarela":
                    ventas_productos = VentaProducts.objects.filter(venta=venta)
                    for item in ventas_productos:
                        cantidad = 0
                        if item.by_venta_caja:
                            cantidad = item.producto.cantidad_cajas * item.cantidad
                        elif item.by_mayor:
                            cantidad = item.producto.cantidad_cajas_prefer * item.cantidad
                        else:
                            cantidad = item.cantidad
                        item.producto.cantidad += cantidad
                        item.producto.save()
                venta.estado = "rechazado"
            else:
                if venta.estado == "proceso":
                    ventas_productos = VentaProducts.objects.filter(venta=venta)
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
                venta.estado = "espera_respuesta_pasarela"

        elif venta.tipo_pasarela.origen == 1 or venta.tipo_pasarela.origen == 2:
            if venta.estado == "proceso":
                venta.estado = "espera_respuesta_pasarela"
                ventas_productos = VentaProducts.objects.filter(venta=venta)
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

        if venta.cliente.email:
            send_invoice(venta.cliente.email, venta, ventas_productos)
            const = Constante.objects.filter(nombre="email_notificacion").first()
            email_notification = const.valor_tipo
            send_invoice(email_notification, venta, ventas_productos)
        venta.save()
        return render(
            request,
            "base/redirect_payment.html",
            context={"page_name": self.page_name, "venta": venta},
        )


class paymentView(View):
    page_name = "Resumen de la compra"

    def post(self, request, *args, **kwargs):
        print(request.POST.get("productos"))
        json_data = json.loads(request.POST.get("productos"))
        print(json_data)
        mp = mercadopago.MP(MERCADOPAGO_ACCESS_TOKEN)
        items = []
        total = 0
        cantidad_total = 0

        try:
            client = Cliente.objects.get(cedula=request.POST.get("document"))
            client.email = request.POST.get("email")
            client.locacion = request.POST.get("locacion")
            client.nombre = request.POST.get("full_name")
            client.telefono = request.POST.get("phone")
            client.direccion = request.POST.get("address")
        except Cliente.DoesNotExist:
            client = Cliente(
                cedula=request.POST.get("document"),
                locacion=request.POST.get("locacion"),
                nombre=request.POST.get("full_name"),
                email=request.POST.get("email"),
                telefono=request.POST.get("phone"),
                direccion=request.POST.get("address"),
            )

        client.save()

        ventas = Venta(cliente=client)
        ventas.save()
        for item in json_data:
            producto = Producto.objects.get(id=int(item["id"]))

            total += int(item["precio"]) * int(item["cantidad"])
            total += int(item["precio_caja"]) * int(item["cantidad_cajas"])
            total += int(item["precio_xmayor"]) * int(item["cantidad_xmayor"])

            if int(item["cantidad"]) > 0:
                items.append(
                    {
                        "title": f"{producto.nombre} {producto.descripcion_no_prefer}",
                        "quantity": int(item["cantidad"]),
                        "currency_id": "COP",
                        "unit_price": int(item["precio"]),
                    }
                )
                products = VentaProducts(
                    venta=ventas,
                    producto_id=item["id"],
                    cantidad=int(item["cantidad"]),
                    precio=int(item["precio"]),
                    especificaciones=item["especificaciones"],
                    by_venta_caja=False,
                )
                products.save()

            if int(item["cantidad_cajas"]) > 0:
                items.append(
                    {
                        "title": f"{producto.nombre} {producto.descripcion_adicional}",
                        "quantity": int(item["cantidad_cajas"]),
                        "currency_id": "COP",
                        "unit_price": int(item["precio_caja"]),
                    }
                )
                products = VentaProducts(
                    venta=ventas,
                    producto_id=item["id"],
                    cantidad=int(item["cantidad_cajas"]),
                    precio=int(item["precio_caja"]),
                    especificaciones=item["especificaciones"],
                    by_venta_caja=True,
                )
                products.save()

            if int(item["cantidad_xmayor"]) > 0:
                items.append(
                    {
                        "title": f"{producto.nombre} {producto.descripcion_prefer}",
                        "quantity": int(item["cantidad_xmayor"]),
                        "currency_id": "COP",
                        "unit_price": int(item["precio_xmayor"]),
                    }
                )
                products = VentaProducts(
                    venta=ventas,
                    producto_id=item["id"],
                    cantidad=int(item["cantidad_xmayor"]),
                    precio=int(item["precio_xmayor"]),
                    especificaciones=item["especificaciones"],
                    by_venta_caja=False,
                    by_mayor=True,
                )
                products.save()

        pasarela = Pasarelas.objects.filter(activo=True).first()
        response = None
        wompi = None
        epayco = None
        url_redirect = ""
        url_response = ""
        url_mercadopgos = ""
        if pasarela.origen == 0:
            preference = {
                "external_reference": ventas.id,
                "items": items,
                "back_urls": {
                    "success": f"https://www.farsalicolombia.com/redirect_pago/{ventas.id}/?success=1",
                    "failure": f"https://www.farsalicolombia.com/redirect_pago/{ventas.id}/?failure=1",
                    "pending": f"https://www.farsalicolombia.com/redirect_pago/{ventas.id}/",
                },
                "auto_return": "approved",
            }
            create_preference_result = mp.create_preference(preference)
            print(create_preference_result)
            response = create_preference_result["response"]["id"]
            url_mercadopgos = create_preference_result["response"]["init_point"]
            ventas.referencia_pasarela = response
        elif pasarela.origen == 1:
            response = ventas.referencia
            wompi = WOMPI_PUBLIC_KEY
            url_redirect = f"https://www.farsalicolombia.com/redirect_pago/{ventas.id}/"

        elif pasarela.origen == 2:
            response = ventas.referencia
            epayco = EPAYCO_PUBLIC_KEY
            url_redirect = f"https://www.farsalicolombia.com/redirect_pago/{ventas.id}/"
            url_response = f"https://www.farsalicolombia.com/redirect_pago/{ventas.id}/"

        ventas.tipo_pasarela = pasarela
        ventas.total = total
        ventas.save()
        return render(
            request,
            "base/summary_payment.html",
            context={
                "venta_id": ventas.id,
                "page_name": self.page_name,
                "preference": response,
                "pasarela": pasarela.origen,
                "wompi": wompi,
                "epayco": epayco,
                "products": items,
                "total": total,
                "client": client,
                "url_mercadopgos": url_mercadopgos,
                "url_response": url_response,
                "url_redirect": url_redirect,
            },
        )


class registerFarsali(TemplateView):
    template_name = "base/register-farsali.html"
    page_name = "Registro Clientes Farsali"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"page_name": self.page_name})
        return context


class recoverypasswordFarsali(TemplateView):
    template_name = "modules/call-to-action/recovery-password.html"
    page_name = "Recuperacion Contraseña"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"page_name": self.page_name})
        return context


def paymentCashView(request):
    page_name = "Confirmacion de Pago"
    venta = None
    if request.POST:
        venta_id = request.POST.get("venta_id")
        venta = Venta.objects.get(pk=venta_id)
        venta.estado = "pendiente_efectivo"
        venta.metodo_pago = "efectivo"
        venta.save()
        ventas_productos = VentaProducts.objects.filter(venta=venta)
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
        if venta.cliente.email:
            send_invoice(venta.cliente.email, venta, ventas_productos)
            const = Constante.objects.filter(nombre="email_notificacion").first()
            email_notification = const.valor_tipo
            send_invoice(email_notification, venta, ventas_productos)
    return render(
        request, "base/redirect_payment.html", context={"page_name": page_name, "venta": venta}
    )


# callback of the payments


@csrf_exempt
def callbackGatewayWompiView(request):
    print(request.method)
    if request.method == "POST":
        json_data = json.loads(request.body.decode("utf-8"))
        print("WompiCallback")
        print(json_data)
        if json_data["event"] == "transaction.updated":
            data = json_data["data"]["transaction"]
            venta = Venta.objects.get(referencia=data["reference"])
            venta.metodo_pago = data["payment_method_type"]
            venta.transaccion_id = data["id"]
            if data["status"] == "APPROVED" and not (
                venta.estado == "rechazado" or venta.estado == "aprobado"
            ):
                if venta.estado == "proceso":
                    ventas_productos = VentaProducts.objects.filter(venta=venta)
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
                venta.estado = "aprobado"

            elif data["status"] == "DECLINED" and not (
                venta.estado == "rechazado" or venta.estado == "aprobado"
            ):
                if venta.estado == "espera_respuesta_pasarela":
                    ventas_productos = VentaProducts.objects.filter(venta=venta)
                    for item in ventas_productos:
                        cantidad = 0
                        if item.by_venta_caja:
                            cantidad = item.producto.cantidad_cajas * item.cantidad
                        elif item.by_mayor:
                            cantidad = item.producto.cantidad_cajas_prefer * item.cantidad
                        else:
                            cantidad = item.cantidad
                        item.producto.cantidad += cantidad
                        item.producto.save()
                venta.estado = "rechazado"

            else:
                if venta.estado == "espera_respuesta_pasarela":
                    ventas_productos = VentaProducts.objects.filter(venta=venta)
                    for item in ventas_productos:
                        cantidad = 0
                        if item.by_venta_caja:
                            cantidad = item.producto.cantidad_cajas * item.cantidad
                        elif item.by_mayor:
                            cantidad = item.producto.cantidad_cajas_prefer * item.cantidad
                        else:
                            cantidad = item.cantidad
                        item.producto.cantidad += cantidad
                        item.producto.save()
                venta.estado = "error_pasarela"

            venta.save()
            return HttpResponse("Todo ok")
        else:
            return HttpResponse("event not found")
    return HttpResponse("method not allowed")


@csrf_exempt
def callbackGatewayMercadoPagoView(request):
    print(request.method)
    if request.method == "POST":
        topic = request.GET.get("topic") if request.GET.get("topic") else None
        payment_id = request.GET.get("id") if request.GET.get("id") else None
        if topic and payment_id:
            url_mercadopago = MERCADOPAGO_URL + payment_id
            headers = {"Authorization": "Bearer " + MERCADOPAGO_ACCESS_TOKEN}
            response = requests.get(url_mercadopago, headers=headers)
            print(response)
            if response.status_code == 200:
                data_json = response.json()
                print(data_json)
                venta = Venta.objects.get(pk=data_json["external_reference"])
                if data_json["status"] == "approved" and not (
                    venta.estado == "rechazado" or venta.estado == "aprobado"
                ):
                    if venta.estado == "proceso":
                        ventas_productos = VentaProducts.objects.filter(venta=venta)
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
                    venta.estado = "aprobado"

                elif data_json["status"] == "rejected" and not (
                    venta.estado == "rechazado" or venta.estado == "aprobado"
                ):
                    if venta.estado == "espera_respuesta_pasarela":
                        ventas_productos = VentaProducts.objects.filter(venta=venta)
                        for item in ventas_productos:
                            cantidad = 0
                            if item.by_venta_caja:
                                cantidad = item.producto.cantidad_cajas * item.cantidad
                            elif item.by_mayor:
                                cantidad = item.producto.cantidad_cajas_prefer * item.cantidad
                            else:
                                cantidad = item.cantidad
                            item.producto.cantidad += cantidad
                            item.producto.save()
                    venta.estado = "rechazado"

                elif data_json["status"] == "cancelled" and not (
                    venta.estado == "rechazado" or venta.estado == "aprobado"
                ):
                    if venta.estado == "espera_respuesta_pasarela":
                        ventas_productos = VentaProducts.objects.filter(venta=venta)
                        for item in ventas_productos:
                            cantidad = 0
                            if item.by_venta_caja:
                                cantidad = item.producto.cantidad_cajas * item.cantidad
                            elif item.by_mayor:
                                cantidad = item.producto.cantidad_cajas_prefer * item.cantidad
                            else:
                                cantidad = item.cantidad
                            item.producto.cantidad += cantidad
                            item.producto.save()
                    venta.estado = "error_pasarela"

                elif data_json["status"] == "pending" and not (
                    venta.estado == "rechazado" or venta.estado == "aprobado"
                ):
                    if venta.estado == "proceso":
                        ventas_productos = VentaProducts.objects.filter(venta=venta)
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
                    venta.estado = "espera_respuesta_pasarela"

                if venta.cliente.email:
                    send_invoice(venta.cliente.email, venta, ventas_productos)
                    const = Constante.objects.filter(nombre="email_notificacion").first()
                    email_notification = const.valor_tipo
                    send_invoice(email_notification, venta, ventas_productos)

                if "payment_method_id" in data_json:
                    venta.metodo_pago = data_json["payment_method_id"]
                venta.save()
            return HttpResponse(status=200)
        return HttpResponse(status=400)
    return HttpResponse(status=500)
