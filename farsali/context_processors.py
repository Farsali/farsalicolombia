# coding: utf-8
from django.conf import settings

from .apps.models import Constante, RedSocial


def farsali(request):
    logged_usser = request.session.get('username', None)
    ctx = {
        'logged_usser': logged_usser,
        'redes_sociales': RedSocial.objects.all(),
        'GOOGLE_KEY_CAPTCHA_V3': settings.GOOGLE_KEY_CAPTCHA_V3,
    }
    constantes = Constante.objects.all()
    constantes_dict = {
        const.nombre: {
            "valor": const.valor_tipo,
            "enlace": const.enlace_texto,
            "icono_svg": const.icono_svg,
            "icono": const.icono,
        } for const in constantes
    }
    telefonos_list = []
    for k, v in constantes_dict.items():
        if 'contacto_telefono' in k:
            telefono_dict = {
                'valor': v.get('valor'),
                'enlace': v.get('enlace'),
                "icono_svg": v.get('icono_svg'),
                "icono": v.get('icono'),
            }
            telefonos_list.append(telefono_dict)
    constantes_dict.update({
        'contacto_telefonos': telefonos_list
    })
    ctx.update(constantes_dict)
    return ctx
