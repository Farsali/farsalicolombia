# coding: utf-8
from django.urls import path

from .views import (
    homeView,
    contactoView,
    videosView,
    nosotrosView,
    redesView,
    politicasView,
    marcasView,
    tiendaView,
    productsDetailView,
    checkoutView,
    paymentClienteView,
    paymentView,
    registerFarsali,
    productsView,
    callbackGatewayWompiView,
    redirectPaymentView
    # ajax_highligths
)

from ..views import (
    ComentarioViewMixin,
    ContactoViewMixin,
    ClienteViewMixin,
    activate_farsali,
    login_farsali,
    logout_farsali
)


urlpatterns = [
    path('', homeView.as_view(), name='home'),
    path('contacto/', ContactoViewMixin.as_view(), name='contacto'),
    path('videos/', videosView.as_view(), name='videos'),
    path('nosotros/', nosotrosView.as_view(), name='nosotros'),
    path('redes/', redesView.as_view(), name='redes'),
    path('politicas/', politicasView.as_view(), name='politicas'),
    path(
        'productos/<int:id_producto>/',
        ComentarioViewMixin.as_view(),
        name='producto_detalle'
    ),
    path('marcas/<pk>/', marcasView.as_view(), name='marcas'),
    path('tienda/', tiendaView.as_view(), name='tienda'),
    path('compra/', checkoutView, name='checkout'),
    path('datos_cliente/', paymentClienteView, name='datos_cliente'),
    path('resumen_pago/', paymentView.as_view(), name='resumen_pago'),
    path('lista_productos/', productsView, name='lista_productos'),

    # callback de las pasarelas de pagos
    path('callback_pago_wompi/', callbackGatewayWompiView, name='callback_pago_wompi'),
    path('redirect_pago/<reference>/', redirectPaymentView.as_view(), name='redirect_pago'),

    path(
        'registro_farsali/',
        ClienteViewMixin.as_view(),
        name='registro_farsali'
    ),
    path(
        'activate_farsali/(?P<unicknameb64>[0-9A-Za-z_\-]+)/',
        activate_farsali,
        name='activate_farsali'
    ),
    path(
        'login/',
        login_farsali,
        name='login_farsali'
    ),
    path(
        'logout/',
        logout_farsali,
        name='logout_farsali'
    )
    # path('pagination/', ajax_highligths, name='ajax_highligths'),
]
