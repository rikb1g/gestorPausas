from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Filtra um item em um dicionário baseado na chave."""
    return dictionary.get(key)