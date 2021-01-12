# coding: utf-8
import os
import json
import decimal
from django.conf import settings
from django.utils.safestring import mark_safe

from django import template

register = template.Library()


@register.simple_tag
def json_serialize(objects_list):
    u"""
    Este template tag hacer un dump de objetos que llegan
    desde el backend y pasarlo a pluggins basados en JavaScript
    para su mejor manejo y interpretación
    :return:
        json_objects
    """
    def decimal_default(obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
    json_objects = json.dumps(
        objects_list,
        separators=(',', ': '),
        default=decimal_default)

    return json_objects


@register.simple_tag
def multiply(qty, unit_price, format_price=True, *args, **kwargs):
    # you would need to do any localization of the result here
    value = int(qty) * int(unit_price)
    if format_price:
        return  "{:,.0f}".format(value).replace(',','.')
    return value


@register.simple_tag
def include_svg(svg_path):
    """
    Returns the content of the file
    """
    try:
        content = svg_path.read()
    except Exception as e:
        if settings.DEBUG:
            print(str(e))
        content = None

    return mark_safe(content)
