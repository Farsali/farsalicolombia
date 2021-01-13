
# coding: utf-8
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.db.models import F
from django.core.paginator import Paginator
from django.http import JsonResponse
from ..inventario.models import Producto, CategoriaProducto, Comentario, Marca
from ..models import Generic, Background, Pasarelas
from django.views.generic.base import View

from farsali.apps.clientes.models import Cliente
from farsali.apps.ventas.models import Venta, VentaProducts

import mercadopago
import json
from farsali.settings import MERCADOPAGO_ACCESS_TOKEN, WOMPI_PUBLIC_KEY, EPAYCO_PUBLIC_KEY

from django.views.generic import ListView


def dict_producto(producto):
    fotos = [{
        'nombre': foto.nombre,
        'imagen': {
            'url': foto.imagen.url if foto.imagen else None
        },
    } for foto in producto.galeria_producto.all()]
    if not fotos:
        fotos = [{
            'nombre': producto.nombre,
            'imagen': {
                'url': producto.imagen.url if producto.imagen else None,
            }
        }]

    # Comentarios del producto
    comentarios = [{
        'nombre_cliente': comentario.nombre,
        'ciudad': comentario.ciudad,
        'comentario': comentario.comentario,
        'titulo': comentario.titulo,
        'fecha': comentario.creado
    } for comentario in producto.comentario_producto.filter(estado=1).order_by("orden","creado")]

    product_dict = {
        'id': producto.id,
        'nombre': producto.nombre,
        'orden': producto.orden,
        'descripcion': producto.descripcion,
        'descripcion_adicional': producto.descripcion_adicional if producto.descripcion_adicional else "",
        'descripcion_no_prefer': producto.descripcion_no_prefer if producto.descripcion_no_prefer else "",
        'descripcion_prefer': producto.descripcion_prefer if producto.descripcion_prefer else "",
        'categoria_id': producto.categoria_id,
        'codigo': producto.codigo,
        'imagen': producto.imagen,
        'calificacion': producto.calificacion,
        'cantidad_cajas': producto.cantidad_cajas,
        'costo_adicional': producto.costo_adicional,
        'costo': producto.costo,
        'costo_farsali': producto.costo_farsali,
        'categoria_url': producto.categoria.url,
        'url_video': producto.codigo_video,
        'fotos': fotos,
        'comentarios': comentarios
    }

    return product_dict


def get_productos(**kwargs):
    fields = [
        'id',
        'nombre',
        'descripcion',
        'categoria_id',
        'codigo',
        'imagen',
        'calificacion',
        'costo',
        'cantidad_cajas'
    ]
    map_fields = {
        'categoria_url': F('categoria__url'),
    }
    filter_kwargs = {
        'activo': True,
        'destacado': False
    }
    exclude = {}
    if kwargs.get('filter'):
        filter_kwargs.update(kwargs.get('filter'))
    if kwargs.get('exclude'):
        exclude.update(kwargs.get('exclude'))
    #TODO quitarlo en la noche
    productos_qs = Producto.objects.filter(**filter_kwargs).exclude(**exclude)[:40]
    productos = productos_qs.values(*fields, **map_fields)
    for p in productos:
        p['calificacion_cantidad'] = range(
            0, p['calificacion']+1) if p.get('calificacion') else []
    return productos


def get_generics(**kwargs):
    filter_kwargs = {
        'activo': True
    }
    if kwargs.get('filter'):
        filter_kwargs.update(kwargs.get('filter'))
    generics = Generic.objects.filter(**filter_kwargs)
    if kwargs.get('exclude'):
        filter_kwargs.update(kwargs.get('exclude'))
    generics = Generic.objects.filter(**filter_kwargs)
    return generics


def get_backgrounds(**kwargs):
    filter_kwargs = {
        'activo': True
    }
    if kwargs.get('filter'):
        filter_kwargs.update(kwargs.get('filter'))
    productos_qs = Producto.objects.filter(**filter_kwargs)
    if kwargs.get('exclude'):
        productos_qs.exclude(**kwargs.get('exclude'))
    background = Background.objects.filter(**filter_kwargs).first()
    return background


def get_marcas(**kwargs):
    filter_kwargs = {
        'activo': True
    }
    marcas = Marca.objects.filter(**filter_kwargs).order_by("orden")
    return marcas


def productsView(request):
    page_number = request.GET.get('page')
    quantity = 10
    pagination=int(page_number)*quantity

    fields = [
        'id',
        'nombre',
        'descripcion',
        'categoria_id',
        'codigo',
        'imagen',
        'calificacion',
        'costo',
        'cantidad_cajas'
    ]
    map_fields = {
        'categoria_url': F('categoria__url'),
    }
    filter_kwargs = {
        'activo': True,
        'destacado': False
    }
    
    productos_qs = Producto.objects.filter(**filter_kwargs)[int(pagination):int(pagination)+quantity]
    productos = productos_qs.values(*fields, **map_fields)
    for p in productos:
        print("/"*30)
        print(p.calificacion)
        print(p['calificacion'])
        p['calificacion_cantidad'] = range(
            0, p['calificacion']+1) if p.get('calificacion') else []
    return JsonResponse({'error':False,'data':list(productos)}, status=200 ,safe=False)


class homeView(TemplateView):
    template_name = "base/home.html"
    page_name = 'home'

    def paginate_highlights(self, context):
        productos_qs = Producto.objects.filter(activo=True)
        my_model = productos_qs.filter(
            destacado=True)
        number_of_item = 6
        paginatorr = Paginator(my_model, number_of_item)
        first_page = paginatorr.page(1).object_list
        page_range = paginatorr.page_range
        context.update({
            'paginatorr': paginatorr,
            'first_page': first_page,
            'page_range': page_range,
            'marcas': get_marcas(),
            'background': get_backgrounds(
                filter={'codigo': self.request.resolver_match.url_name}),
        })
        if self.request.method == 'POST':
            page_n = self.request.POST.get('page_n', None)
            results = list(paginatorr.page(page_n).object_list)
            return JsonResponse({"results": results})
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        productos_qs = get_productos()
        productos_hg = get_productos(**{
            'filter': {
                'destacado': True
            }
        })
        categorias_qs = CategoriaProducto.objects.all()
        context.update({
            'page_name': self.page_name,
            'productos': productos_qs,
            'productos_destacados': productos_hg,
            'marcas': get_marcas(),
            'categorias': categorias_qs,
            'background': get_backgrounds(
                filter={'codigo': self.request.resolver_match.url_name}),
        })
        return context


class contactoView(TemplateView):
    template_name = "base/contacto.html"
    page_name = 'contacto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_name': self.page_name,
            'marcas': get_marcas(),
            'background': get_backgrounds(
                filter={'codigo': self.request.resolver_match.url_name}),
        })
        return context


class marcasView(TemplateView):
    template_name = "base/marcas.html"
    page_name = 'marcas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            marca = Marca.objects.get(pk=self.kwargs['pk'])
        except Marca.DoesNotExist:
            raise Http404("Marca no existe")

        productos_marca = get_productos(**{
            'filter': {
                'marca_producto': marca
            }
        })
        context.update({
            'page_name': self.page_name,
            'marcas': get_marcas(),
            'marca': marca,
            'productos': productos_marca,
            'background': get_backgrounds(
                filter={'codigo': self.request.resolver_match.url_name}),
        })
        return context


class redesView(TemplateView):
    template_name = "base/redes.html"
    page_name = 'redes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'page_name': self.page_name})
        return context


class nosotrosView(TemplateView):
    template_name = "base/nosotros.html"
    page_name = 'nosotros'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        generics = get_generics(filter={'codigo': self.request.resolver_match.url_name})
        context.update({
            'page_name': self.page_name,
            'generics': generics,
            'marcas': get_marcas(),
            'background': get_backgrounds(
                filter={'codigo': self.request.resolver_match.url_name}),
        })
        return context


class tiendaView(TemplateView):
    template_name = "base/tienda.html"
    page_name = 'tienda'

    def get_context_data(self, **kwargs):
        productos_qs = get_productos()
        productos_hg = get_productos(**{
            'filter': {
                'destacado': True
            }
        })
        categorias_qs = CategoriaProducto.objects.all()
        context = super().get_context_data(**kwargs)
        context.update({
            'page_name': self.page_name,
            'productos': productos_qs,
            'productos_destacados': productos_hg,
            'categorias': categorias_qs,
            'marcas': get_marcas(),
            'background': get_backgrounds(
                filter={'codigo': self.request.resolver_match.url_name}),
        })
        return context


class videosView(TemplateView):
    template_name = "base/videos.html"
    page_name = 'videos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        videos = Producto.objects.exclude(
            codigo_video__isnull=True
        ).exclude(
            codigo_video__exact=''
        ).values(
            "codigo_video",
            "nombre"
        )
        context.update({
            'page_name': self.page_name,
            'marcas': get_marcas(),
            'videos': videos
        })
        return context


class politicasView(TemplateView):
    template_name = "base/politicas.html"
    page_name = 'politicas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_code = self.request.resolver_match.url_name
        generics = get_generics(filter={'codigo': page_code})
        context.update({
            'page_name': self.page_name,
            'generics': generics,
            'background': get_backgrounds(
                filter={'codigo': page_code}),
        })
        return context


class productsDetailView(TemplateView):
    template_name = "base/producto_detalle.html"
    page_name = 'Producto Detalle'
    producto = None

    def dispatch(self, request, *args, **kwargs):
        self.producto = get_object_or_404(
            Producto, pk=kwargs.get('id_producto'))
        return super(productsDetailView, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            producto = dict_producto(self.producto)
        except Producto.DoesNotExist:
            producto = None
        productos_qs_gt = get_productos(exclude={'pk': producto['id']}, filter={'orden__gte':producto["orden"]})
        productos_qs_lt = get_productos(exclude={'pk': producto['id']}, filter={'orden__lt':producto["orden"]})
        productos_qs =  list(productos_qs_gt) + list(productos_qs_lt)

        productos_hg = get_productos(**{
            'filter': {
                'destacado': True
            }
        })
        # categorias_qs = CategoriaProducto.objects.all()
        producto['calificacion_cantidad'] = range(
                0, producto['calificacion']+1) if (
                    producto['calificacion']) else []
        context.update({
            'page_name': self.page_name,
            'producto': producto,
            'marcas': get_marcas(),
            'productos': productos_qs,
            'productos_destacados': productos_hg,
            'background': get_backgrounds(
                filter={'codigo': self.request.resolver_match.url_name}),
        })
        return context


class checkoutView(View):
    page_name = 'Compra'

    def get(self, request, *args, **kwargs):
        json_data = json.loads(request.GET["productos"])
        items = []
        total = 0
        for item in json_data:
            total += int(item["precio"])*int(item["cantidad"])
            items.append(
                {
                    "title": item["titulo"],
                    "quantity": int(item["cantidad"]),
                    "currency_id": "COP",
                    "unit_price": int(item["precio"]),
                    "specs": item["especificaciones"],
                    "id": int(item["id"])
                }
            )
        return render(
            request,
            "base/checkout.html",
            context={
                'page_name': self.page_name,
                'products': items,
                'total': total
            }
        )


class paymentClienteView(View):
    page_name = 'Datos del Cliente'

    def get(self, request, *args, **kwargs):
        json_data = json.loads(request.GET["productos"])
        return render(
            request,
            "base/payment_client.html",
            context={
                'page_name': self.page_name,
                'products': json_data
            }
        )


class paymentView(View):
    page_name = 'Resumen de la compra'

    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.POST.get('productos'))
        mp = mercadopago.MP(MERCADOPAGO_ACCESS_TOKEN)
        items = []
        total = 0

        try:
            client = Cliente.objects.get(cedula=request.POST.get('document'))
            client.email = request.POST.get('email')
            client.locacion = request.POST.get('locacion')
            client.nombre = request.POST.get('full_name')
            client.telefono = request.POST.get('phone')
            client.direccion = request.POST.get('address')
        except Cliente.DoesNotExist:
            client = Cliente(
                cedula=request.POST.get('document'),
                locacion=request.POST.get('locacion'),
                nombre=request.POST.get('full_name'),
                email=request.POST.get('email'),
                telefono=request.POST.get('phone'),
                direccion=request.POST.get('address')
            )

        client.save()

        ventas = Venta(cliente=client)
        ventas.save()
        by_box = True if request.POST.get('boxes') else False
        for item in json_data:
            total += int(item["unit_price"])*int(item["quantity"])
            items.append(
                {
                    "title": item["title"],
                    "quantity": int(item["quantity"]),
                    "currency_id": "COP",
                    "unit_price": int(item["unit_price"])
                }
            )
            products = VentaProducts(venta=ventas, producto_id=item["id"], cantidad=int(item["quantity"]),
                                    precio=int(item["unit_price"]), especificaciones=item["specs"], by_venta_caja=by_box)
            products.save()

        pasarela = Pasarelas.objects.filter(activo=True).first()
        response = None
        wompi = None
        epayco = None

        if pasarela.origen == 0:
            preference = {
                "items": items
            }

            create_preference_result = mp.create_preference(preference)
            response = create_preference_result["response"]["id"]
            ventas.referencia_pasarela = response
        elif pasarela.origen == 1:
            response = ventas.referencia
            wompi = WOMPI_PUBLIC_KEY
            url_redirect = ""

        elif pasarela.origen == 2:
            print(EPAYCO_PUBLIC_KEY)
            response = ventas.referencia
            epayco = EPAYCO_PUBLIC_KEY
            url_redirect = ""
            print(epayco)

        ventas.tipo_pasarela = pasarela
        ventas.total = total
        ventas.save()
        return render(
            request,
            "base/summary_payment.html",
            context={
                'page_name': self.page_name,
                'preference': response,
                'pasarela': pasarela.origen,
                'wompi': wompi,
                'epayco': epayco,
                'products': items,
                'total': total,
                "client": client
            }
        )


class registerFarsali(TemplateView):
    template_name = "base/register-farsali.html"
    page_name = 'Registro Clientes Farsali'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'page_name': self.page_name})
        return context
