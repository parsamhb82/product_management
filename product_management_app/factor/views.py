from .models import Factor, FactorItem, Transaction
from .serializers import DiscountSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from product.models import Discount
from .serializers import DiscountSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .permission import IsSuperUser
import uuid

def generate_unique_transaction_code():
    while True:
        code = str(uuid.uuid4())[:16]  # Generate a random 16-character string
        if not Transaction.objects.filter(code=code).exists():
            return code

def generate_unique_factor_code():
    while True:
        code = str(uuid.uuid4())[:16]  # Generate a random 16-character string
        if not Factor.objects.filter(code=code).exists():
            return code


class CreateDiscountView(CreateAPIView):
    serializer_class = DiscountSerializer
    permission_classes = [IsAuthenticated, IsSuperUser]

class ApplyDiscountView(APIView):

    def Post(self, request):
        factor_id = request.get('factor_id')
        discount_id = request.get('discount_id')
        factor = get_object_or_404(Factor, id=factor_id)
        discount = get_object_or_404(Discount, id=discount_id)

        if factor.discount == discount:
            discount_value = factor.factor_discount
            discounted_price = factor.total_price - (factor.total_price * discount_value / 100)
            return Response({
                'original_price': factor.total_price,
                'discounted_price': discounted_price,
                'discount_value': discount_value
            })
        else:
            return Response({'error': 'The code cannot be used.'}, status=status.HTTP_400_BAD_REQUEST)
        


