from .models import Factor, FactorItem, Transaction
from .serializers import DiscountSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from product.models import Discount
from .serializers import DiscountSerializer, TransactionSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .permission import IsSuperUser
import uuid
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView

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
        
class TransactionView(APIView):
    serializer_class = TransactionSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            code = generate_unique_transaction_code()
            factor_id = serializer.validated_data['factor']
            transaction_type = serializer.validated_data['type']
            
            try:
                factor = Factor.objects.get(id=factor_id)
            except Factor.DoesNotExist:
                return Response({'error': 'Factor not found'}, status=status.HTTP_404_NOT_FOUND)
            
            remaining_price = factor.total_price - factor.paid_price
            if amount <= remaining_price:
                factor.paid_price += amount
                Transaction.objects.create(
                    factor=factor, 
                    amount=amount, 
                    code=code, 
                    type=transaction_type
                )

                if factor.paid_price == factor.total_price:
                    factor.is_paid = True
                factor.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Amount exceeds the remaining price'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TransactionList(ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['factor', 'type', 'created_at']
    ordering_fields = ['created_at']

