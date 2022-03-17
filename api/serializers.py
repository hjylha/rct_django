from rest_framework.serializers import ModelSerializer

from ridetypes.models import RideType, RideName
from stalls.models import Product


class RideTypeSerializer(ModelSerializer):
    class Meta:
        model = RideType
        fields = '__all__'


class RideNameSerializer(ModelSerializer):
    class Meta:
        model = RideName
        # fields = '__all__'
        fields = ['name', 'is_visible', 'excitement_modifier',
                  'intensity_modifier', 'nausea_modifier']


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
