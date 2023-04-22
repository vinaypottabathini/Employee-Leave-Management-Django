from django import template
register = template.Library()

@register.filter()
def to_int(value):
   return int(value)

@register.filter(name='subtract')
def subtract(value, arg):
    return arg-value+1


@register.filter(name='change')
def change(value):
    return str(value)
