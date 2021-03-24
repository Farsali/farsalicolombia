# coding: utf-8
import json
import urllib
import urllib.request
from django import forms
from django.contrib import messages
from django.conf import settings
from django.forms.widgets import Textarea
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from .inventario.models import Producto, Comentario
from .clientes.models import Cliente
from .models import Contacto


class ComentarioForm(forms.ModelForm):

    class Meta:
        model = Comentario
        fields = [
            'producto',
            'nombre',
            'email',
            'ciudad',
            'comentario',
        ]

    def __init__(self, *args, **kwargs):
        def erase_field(field):
            self.fields[field].widget.attrs.update({'style': 'display:none'})
            self.fields[field].widget.attrs.update({'required': False})
            self.fields["comentario"].widget.attrs.update({'rows': 3})
            self.fields[field].label = ''
        self.request = kwargs.pop('request', None)
        self.producto_id = kwargs.pop('producto_id', None)
        super(ComentarioForm, self).__init__(*args, **kwargs)
        if self.producto_id:
            self.fields['producto'].initial = get_object_or_404(
                Producto, pk=self.producto_id)
        erase_field('producto')
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean(self):
        super(ComentarioForm, self).clean()

        # get the token submitted in the form
        recaptcha_response = self.request.POST.get('g-recaptcha-response')
        action = self.request.POST.get('g-recaptcha-action')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        payload = {
            'secret': settings.GOOGLE_SECRET_KEY_CAPTCHA_V3,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(payload).encode()
        req = urllib.request.Request(url, data=data)

        # verify the token submitted with the form is valid
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())

        # result will be a dict containing 'contact' and 'action'.
        # it is important to verify both

        # if self.request.META.get('HTTP_HOST') != result.get('hostname'):
        #         raise forms.ValidationError(
        #             _(u'Only humans are allowed to submit this form.'))

        if not result.get("success", False):
            raise forms.ValidationError(
                _(u'Only humans are allowed to submit this form.'))

        if result.get("action") != action and action != 'producto_detalle':  # make sure action matches the one from your template
            raise forms.ValidationError(
                _(u'Only humans are allowed to submit this form.'))

        return self.cleaned_data


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contacto
        fields = [
            'nombre',
            'email',
            'telefono',
            'contenido',
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ContactForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            style_cols = None
            style_rows = None
            if not isinstance(visible.field.widget, Textarea):
                style_class = 'contact-form__form--input'
                style_cols = '20'
                style_rows = '10'
            else:
                style_class = 'contact-form__form--text'
            visible.field.widget.attrs['class'] = style_class
            if style_cols and style_rows:
                visible.field.widget.attrs['rows'] = style_rows
                visible.field.widget.attrs['cols'] = style_cols

    def clean(self):
        super(ContactForm, self).clean()
        # get the token submitted in the form
        recaptcha_response = self.request.POST.get('g-recaptcha-response')
        action = self.request.POST.get('g-recaptcha-action')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        payload = {
            'secret': settings.GOOGLE_SECRET_KEY_CAPTCHA_V3,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(payload).encode()
        req = urllib.request.Request(url, data=data)

        # verify the token submitted with the form is valid
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())

        # result will be a dict containing 'contact' and 'action'.
        # it is important to verify both

        # if self.request.META.get('HTTP_HOST') != result.get('hostname'):
        #         raise forms.ValidationError(
        #             _(u'Only humans are allowed to submit this form.'))

        if not result.get("success", False):
            raise forms.ValidationError(
                _(u'Only humans are allowed to submit this form.'))

        if result.get("action") != action and action != 'contacto':  # make sure action matches the one from your template
            raise forms.ValidationError(
                _(u'Only humans are allowed to submit this form.'))

        return self.cleaned_data


class ClienteForm(forms.ModelForm):
    contrasena = forms.CharField(widget=forms.PasswordInput)
    confirmar_contrasena = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ClienteForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Cliente
        fields = (
            'nombre',
            'cedula',
            'nick_name',
            'contrasena',
            'confirmar_contrasena',
            'telefono',
            # 'edad',
            'locacion',
            # 'empresa',
            'email',
        )

    def clean_passwords(self, cleaned_data):
        cleaned_data = super(ClienteForm, self).clean()
        contrasena = cleaned_data.get("contrasena")
        confirmar_contrasena = cleaned_data.get("confirmar_contrasena")

        if contrasena != confirmar_contrasena:
            raise forms.ValidationError(
                "Las contraseñas no coinsiden; por favor verificar"
            )

    def clean_usser(self, cleaned_data):
        clean_nick_name = cleaned_data.get('nick_name')
        try:
            usuario = Cliente.objects.get(nick_name=clean_nick_name)
        except ObjectDoesNotExist:
            usuario = None
        if usuario:
            raise forms.ValidationError(
                "El Nick name de usuario ya existe en nuestra base de datos"
            )

    def clean_cedulas(self, cleaned_data):
        clean_cedulas_value = cleaned_data.get('cedula')
        try:
            usuario = Cliente.objects.get(cedula=clean_cedulas_value)
        except ObjectDoesNotExist:
            usuario = None
        if usuario:
            raise forms.ValidationError(
                "La cédula que intenta ingresar ya existe en nuestro sistema"
            )

    def clean(self):
        cleaned_data = super(ClienteForm, self).clean()
        if self.request.method == "POST":
            self.clean_passwords(cleaned_data)
            self.clean_usser(cleaned_data)
            self.clean_cedulas(cleaned_data)

        # get the token submitted in the form
        recaptcha_response = self.request.POST.get('g-recaptcha-response')
        action = self.request.POST.get('g-recaptcha-action')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        payload = {
            'secret': settings.GOOGLE_SECRET_KEY_CAPTCHA_V3,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(payload).encode()
        req = urllib.request.Request(url, data=data)

        # verify the token submitted with the form is valid
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())

        # result will be a dict containing 'contact' and 'action'.
        # it is important to verify both

        # if self.request.META.get('HTTP_HOST') != result.get('hostname'):
        #         raise forms.ValidationError(
        #             _(u'Only humans are allowed to submit this form.'))

        if not result.get("success", False):
            raise forms.ValidationError(
                _(u'Only humans are allowed to submit this form.'))

        if result.get("action") != action and action != 'registro_farsali':  # make sure action matches the one from your template
            raise forms.ValidationError(
                _(u'Only humans are allowed to submit this form.'))

        return self.cleaned_data
