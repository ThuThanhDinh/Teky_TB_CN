from django import template
register = template.Library()

@register.filter
def vn_currency(value):
    try:
        n = int(float(value))
    except (ValueError, TypeError):
        return value
    s = f"{n:,}"
    return s.replace(",", ".")

# Usage in template:
# {% load vn_currency %}
# {{ price|vn_currency }}