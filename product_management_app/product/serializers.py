from rest_framework.serializers import ModelSerializer
from .models import *

class CreateProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'stock', 'image']

class ProductSerilizer(ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"