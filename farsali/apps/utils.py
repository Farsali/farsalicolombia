# coding: utf-8
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
import random

from datetime import datetime

from weasyprint import HTML
from io import BytesIO
from django.template.loader import get_template
from django.core.files.base import ContentFile


def send_mail_farsali(contx, request):
    titulo = str('FORMULARIO DE CONFIRMACIÓN CLIENTE FARSALI')
    template = 'modules/email/farsali_confirmation_email.html'
    html = render_to_string(template, contx)
    origin_mail = settings.DEFAULT_FROM_EMAIL
    destiny_mail = settings.DEFAULT_FROM_EMAIL
    email = EmailMessage(titulo, html, origin_mail, [destiny_mail])
    email.content_subtype = 'html'
    email.send()

    titulo_to_client = str('FORMULARIO DE PRE CONFIRMACIÓN CLIENTE FARSALI')
    template_to_client = 'modules/email/client_pre_confirmation.html'
    html_to_client = render_to_string(template_to_client, contx)
    origin_mail_to_client = settings.DEFAULT_FROM_EMAIL
    destiny_mail_to_client = contx.get('email', settings.DEFAULT_FROM_EMAIL)
    email_to_client = EmailMessage(
        titulo_to_client,
        html_to_client,
        origin_mail_to_client,
        [destiny_mail_to_client]
    )
    email_to_client.content_subtype = 'html'
    email_to_client.send()


def generate_random_chars(length, characters_allowed: str = 'ABCDEFHILKMNPQRSTUVWXYZ12345789'):
    while True:
        chars = ''.join(random.choice(characters_allowed) for _ in range(length))
        if chars.startswith('0'):
            pass
        else:
            return chars


def send_invoice(email, venta, products):

    template = get_template("reports/ventas.html")
    html_template = template.render({
        "reference": venta.referencia,
        "date_now":  datetime.now().strftime("%d de %m del %Y"),
        "name_client": venta.cliente.nombre,
        "document_client": venta.cliente.cedula,
        "address": venta.cliente.direccion,
        "location": venta.cliente.locacion,
        "phone": venta.cliente.telefono,
        "price": "{:,.0f}".format(venta.total).replace(',','.'),
        "products": products
    })
    response = BytesIO()
    html = HTML(string=html_template.encode("UTF-8"))
    html.write_pdf(response)

    subject = 'Farsali - Factura de compra'
    body = ""
    from_email = settings.DEFAULT_FROM_EMAIL
    email = EmailMessage(subject, body, from_email, [email])
    email.content_subtype = "html"

    email.attach('factura.pdf', response.getvalue(), 'application/pdf')

    email.send()
