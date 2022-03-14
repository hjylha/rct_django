
from .models import Product


def get_viewable_products():
    products_raw = list(Product.objects.all())
    products = []
    for raw_product in products_raw:
        product = {
            'name': raw_product.name,
            'buy_during_rain': raw_product.buy_during_rain,
            'cost': int(raw_product.cost) / 100,
            'price_base': int(raw_product.price_base) / 100,
            'price_hot': int(raw_product.price_hot) / 100,
            'price_cold': int(raw_product.price_cold) / 100,
            'price_initial': int(raw_product.price_initial) / 100
        }
        products.append(product)
    return products
    