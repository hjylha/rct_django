from django.shortcuts import render

from .models import Product

# Create your views here.

def product_table_view(request, *args, **kwargs):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'stalls/stall_overview.html', context)
