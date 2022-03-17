from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from ridetypes.models import RideType, RideName
from stalls.models import Product
from .serializers import RideTypeSerializer, RideNameSerializer, ProductSerializer

# Create your views here.

@api_view(['GET'])
def OverviewAPI(request):
    stuff = [
        'GET /api',
        'GET /api/ridetypes',
        'GET /api/ridetypes/?ridename=searchterm',
        'GET /api/products',
        'GET /api/products/?product=searchterm'
    ]
    return Response(stuff)


@api_view(['GET'])
def get_ridenames(request):
    ridename = request.GET.get('ridename')
    if ridename:
        ridenames = RideName.objects.filter(name__icontains=ridename)
    # if no searchterm, get everything
    else:
        ridenames = RideName.objects.all()
    
    returned_data = []
    for ride in ridenames:
        serialized_ride = RideNameSerializer(ride, many=False)
        ride_dict = serialized_ride.data
        ride_dict['ridetype'] = RideTypeSerializer(ride.ridetype, many=False).data
        returned_data.append(ride_dict)

    # serialized_ridenames = RideNameSerializer(ridenames, many=True)
    # print(serialized_ridenames.data)
    # return Response(serialized_ridenames.data)
    
    return Response(returned_data)

@api_view(['GET'])
def get_products(request):
    product_name = request.GET.get('product')
    if product_name:
        products = Product.objects.filter(name__icontains=product_name)
    else:
        products = Product.objects.all()

    serialized_products = ProductSerializer(products, many=True)

    return Response(serialized_products.data)