from django.shortcuts import render

from .models import Product
from .utils import get_viewable_products

# Create your views here.

def product_table_view(request, *args, **kwargs):
    # products = Product.objects.all()
    products = get_viewable_products()
    context = {
        'products': products
    }
    return render(request, 'stalls/stall_overview.html', context)
