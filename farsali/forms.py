# coding: utf-8
from django import forms
from django.core.exceptions import ValidationError


class ImagenAdminForm(forms.ModelForm):
    def clean_imagen(self):
        imagen = self.cleaned_data["imagen"]
        if imagen:
            try:
                imagen.name.encode("ascii")
            except UnicodeEncodeError:
                raise ValidationError(_("Nombre de archivo incorrecto"))
        return self.cleaned_data["imagen"]
