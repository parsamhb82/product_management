from django.shortcuts import render
from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView , ListAPIView)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .serializers import Productserializer
from .models import Product
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAdminUser, IsAuthenticated , AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

class login(TokenObtainPairView):
    pass


class refresh(TokenRefreshView):
    pass

class AddProduct(ListCreateAPIView):
    queryset =  Product.objects.all()
    serializer_class = Productserializer
    permission_classes = [IsAdminUser]
    def perform_create(self, serializer):
        owner = serializer.save(owner = self.request.user)
        return owner
class EditProduct(RetrieveUpdateDestroyAPIView):
    queryset =  Product.objects.all()
    serializer_class = Productserializer
    filter_backends = [DjangoFilterBackend , filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["price", "stock"]
    search_fields = ["name"]
    filterset_fields = ["category"]
    permission_classes = [IsAdminUser]
    
    
# Create your views here.
