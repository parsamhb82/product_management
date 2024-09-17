from .models import Factor, FactorItem
from .serializers import DiscountSerializer
from rest_framework.views import APIView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Factor
from django.shortcuts import get_object_or_404
from product.models import Discount
from .serializers import DiscountSerializer
from rest_framework.generics import CreateAPIView

class CreteDiscountView(CreateAPIView):
    serializer_class = DiscountSerializer

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
        


