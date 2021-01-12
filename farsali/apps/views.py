# coding: utf-8
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from django.views.generic.edit import FormMixin
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from .forms import (
    ComentarioForm,
    ContactForm,
    ClienteForm
)
from .clientes.models import Cliente
from .utils import send_mail_farsali

from .navegacion.views import (
    productsDetailView,
    contactoView,
    registerFarsali
)


def error_404(request, exception):
    return render(request,'base/404.html')


class ComentarioViewMixin(FormMixin, productsDetailView):
    form_class = ComentarioForm
    producto = None

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        self.response = True
        messages.add_message(self.request, messages.SUCCESS, 'El comentario fue agregado exitosamente!')
        return super(ComentarioViewMixin, self).form_valid(form)

    def get_context_data(self, **kwargs):
        data = super(ComentarioViewMixin, self).get_context_data(**kwargs)
        data['form'] = self.get_form()

        return data

    def get_form_kwargs(self):
        kwargs = super(ComentarioViewMixin, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
            'producto_id': self.producto.id,
        })
        return kwargs

    def get_success_url(self):
        msg = "ok"
        id_producto = self.request.resolver_match.kwargs.get('id_producto')
        return "{}?msg={}".format(
            reverse(
                'producto_detalle',
                kwargs={'id_producto': id_producto}
            ),
            msg
        )


class ContactoViewMixin(FormMixin, contactoView):
    form_class = ContactForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        self.response = True
        messages.add_message(self.request, messages.SUCCESS, 'El mensaje fue enviado exitosamente!')
        return super(ContactoViewMixin, self).form_valid(form)

    def get_context_data(self, **kwargs):
        data = super(ContactoViewMixin, self).get_context_data(**kwargs)
        data['form'] = self.get_form()

        return data

    def get_form_kwargs(self):
        kwargs = super(ContactoViewMixin, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs

    def get_success_url(self):
        msg = "ok"
        return "{}?msg={}".format(
            reverse('contacto'),
            msg
        )


class ClienteViewMixin(FormMixin, registerFarsali):
    form_class = ClienteForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        current_site = get_current_site(self.request)
        ctx = {
            'nombre': form.cleaned_data['nombre'],
            'nick_name': form.cleaned_data['nick_name'],
            'contrasena': form.cleaned_data['contrasena'],
            'telefono': form.cleaned_data['telefono'],
            # 'edad': form.cleaned_data['edad'],
            'locacion': form.cleaned_data['locacion'],
            # 'empresa': form.cleaned_data['empresa'],
            'email': form.cleaned_data['email'],
            'unickname': urlsafe_base64_encode(
                force_bytes(form.cleaned_data['nick_name'])),
            'domain': current_site.domain,
        }
        send_mail_farsali(ctx, self.request)
        form.save()
        self.response = True
        messages.add_message(self.request, messages.SUCCESS, 'Se ha enviado tu solicitud de registro y ahora esta en proceso de revisión!')
        return super(ClienteViewMixin, self).form_valid(form)

    def get_context_data(self, **kwargs):
        data = super(ClienteViewMixin, self).get_context_data(**kwargs)
        data['form'] = self.get_form()

        return data

    def get_form_kwargs(self):
        kwargs = super(ClienteViewMixin, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs

    def get_success_url(self):
        msg = "ok"
        return "{}?msg={}".format(
            reverse('registro_farsali'),
            msg
        )


def activate_farsali(request, unicknameb64):
    try:
        unickname = force_text(urlsafe_base64_decode(unicknameb64))
        cliente = Cliente.objects.get(nick_name=unickname)
    except(TypeError, ValueError, OverflowError, Cliente.DoesNotExist):
        cliente = None

    if cliente:
        cliente.is_farsali = True
        cliente.fecha_activacion = timezone.now()
        cliente.save()
        titulo = str('FORMULARIO DE PRE CONFIRMACIÓN CLIENTE FARSALI')
        template = 'modules/email/client_post_confirmation.html'
        html = render_to_string(template, {'nombre': cliente.nombre})
        origin_mail = settings.DEFAULT_FROM_EMAIL
        destiny_mail = cliente.email
        email = EmailMessage(titulo, html, origin_mail, [destiny_mail])
        email.content_subtype = 'html'
        email.send()
        return HttpResponse(
            'Activación realizada'
        )
    else:
        return HttpResponse(
            'Activación inválida'
        )


def login_farsali(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        msg = 'logged'
        try:
            cliente = Cliente.objects.get(
                nick_name=username)
            if not cliente.activo:
                messages.add_message(request, messages.ERROR, 'El usuario está inactivo; por favor colocarse en contacto con nosotros')
                msg = 'inactivated'
                return HttpResponseRedirect(
                    "{}?msg={}".format(
                        reverse('home'),
                        msg
                    )
                )
            if not check_password(password, cliente.contrasena):
                messages.add_message(request, messages.ERROR, 'El usuario o contraseña no inválido!')
                msg = 'invalid'
                return HttpResponseRedirect(
                    "{}?msg={}".format(
                        reverse('home'),
                        msg
                    )
                )
        except (TypeError, ValueError, OverflowError, Cliente.DoesNotExist):
            messages.add_message(request, messages.ERROR, 'El cliente no existe!')
            msg = 'inexistent'
            return HttpResponseRedirect(
                "{}?msg={}".format(
                    reverse('home'),
                    msg
                )
            )
            
        if not cliente.is_farsali:
            messages.add_message(request, messages.ERROR, 'El cliente se encuentra inactivo!')
            msg = 'inactived'
            return HttpResponseRedirect(
                "{}?msg={}".format(
                    reverse('home'),
                    msg
                )
            )
        
        request.session['username'] = cliente.nick_name
        messages.add_message(request, messages.SUCCESS, 'El cliente ha iniciado sessión exitosamente!')
        return HttpResponseRedirect(
            "{}?msg={}".format(
                reverse('home'),
                msg
            )
        )


def logout_farsali(request):
    user = request.session.get('username')
    msg = 'logout'
    if user:
        del request.session['username']
        messages.add_message(request, messages.SUCCESS, 'El cliente ha cerrado sessión exitosamente!')
        return HttpResponseRedirect(
            "{}?msg={}".format(
                reverse('home'),
                msg
            )
        )
