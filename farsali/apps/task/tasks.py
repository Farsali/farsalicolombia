import random
from io import BytesIO

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
from farsali.apps.inventario.models import GaleriaProducto
from farsali.celery import app
from weasyprint import HTML


@app.task(priority=0)
def send_email_pdf_products(products_id):
    email = settings.DEFAULT_FROM_EMAIL
    queryset = GaleriaProducto.objects.filter(pk__in=products_id)
    template = get_template("reports/imagenes_products.html")
    html_template = template.render({"data_imagenes": list(queryset)})
    response = BytesIO()
    html = HTML(string=html_template.encode("UTF-8"))
    html.write_pdf(response)
    number = random.randrange(100000)
    filename = f"fotos_{number}.pdf"

    titulo = str("IMAGENES DE LOS PRODUCTOS EN PDF")

    origin_mail = settings.DEFAULT_FROM_EMAIL
    destiny_mail = email
    email = EmailMessage(titulo, "", origin_mail, [destiny_mail])
    email.content_subtype = "html"
    data_attach = {
        "name_file": filename,
        "file": response.getvalue(),
        "type": "application/pdf",
    }
    email.attach(
        data_attach["name_file"],
        data_attach["file"],
        data_attach["type"],
    )
    email.send()
