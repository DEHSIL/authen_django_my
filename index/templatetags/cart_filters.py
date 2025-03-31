from django import template

register = template.Library()

@register.filter
def cart_filters(carts_product, product):
    """Возвращает объект корзины для данного продукта"""
    return carts_product.filter(product=product).first()

@register.filter
def cart_quantity(carts_product, product):
    """Возвращает количество данного продукта в корзине"""
    cart_item = carts_product.filter(product=product).first()
    return cart_item.quantity if cart_item else 0