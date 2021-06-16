# coding: utf-8
from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from farsali.apps import views

admin.site.index_title = "Welcome to Farsali Researcher Portal"
admin.empty_value_display = "**Empty**"

statics = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

medias = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    path("control/", admin.site.urls),
    path("", include("farsali.apps.navegacion.urls")),
    path("", include("farsali.apps.ventas.urls")),
]

urlpatterns += statics
handler404 = views.error_404
# urlpatterns += medias
