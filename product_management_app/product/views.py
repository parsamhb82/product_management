from django.shortcuts import render
from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView , ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .serializers import *
from .models import Product
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAdminUser, IsAuthenticated , AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
import uuid


def generate_unique_product_code():
    while True:
        code = str(uuid.uuid4())[:16]
        if not Product.objects.filter(code=code).exists():
            return code


class AddProduct(CreateAPIView):
    queryset =  Product.objects.all()
    serializer_class = CreateProductSerializer
    permission_classes = [IsAdminUser]
    def perform_create(self, serializer):
        code = generate_unique_product_code()
        owner = serializer.save(owner = self.request.user.legalperson, code = code)
        
class EditProduct(UpdateAPIView):
    queryset =  Product.objects.all()
    serializer_class = CreateProductSerializer

    def get_queryset(self):
        return Product.objects.filter(owner = self.request.user.legalperson)

class ListProductView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerilizer
    filter_backends = [DjangoFilterBackend , filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["price", "stock"]
    search_fields = ["name"]
    filterset_fields = ["category"]

class DestroyProductView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerilizer
    def get_queryset(self):
        return Product.objects.filter(owner = self.request.user.legalperson)

    
    
# Create your views here.
