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

from rest_framework.generics import ListAPIView
from .serializers import FactorViewSerilizer
from .serializers import FactorSerializer
from product.models import Product
from django.utils import timezone


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

class CreatFactor(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FactorSerializer

    def post(self, request):
        try :

            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                products = validated_data.get('products')
                quantities = validated_data.get('quantities')
                discount_code = validated_data.get('discount_code','')
                if discount_code == '':
                    bill = 0
                    for i in range(len(products)):
                        if products[i].quantity < quantities[i]:
                            return Response({'error': 'The quantity of the product is not enough.'}, status=status.HTTP_400_BAD_REQUEST)
                        bill += products[i].price * quantities[i]
                        bill = bill * 1.1 # 10% tax
                
                    factor = Factor.objects.create(
                        user=request.user,
                        code=generate_unique_factor_code(),
                        total_price=bill,
                    )
                    for i in range(len(products)):
                        FactorItem.objects.create(
                            factor=factor,
                            product=products[i],
                            quantity=quantities[i],
                            price = products[i].price,
                            total_price=products[i].price * quantities[i])
                        products[i].quantity -= quantities[i]
                        products[i].save()
                    return Response({'message': 'The factor has been successfully created.'}, status=status.HTTP_201_CREATED)
                
                elif discount_code != '':
                    discount = get_object_or_404(Discount, code=discount_code)
                    time = timezone.now()
                    if discount.end < time:
                        return Response ({'error': 'The discount code has expired.'}, status=status.HTTP_400_BAD_REQUEST)
                    

                    if discount.all_products and discount.all_customers:
                        bill = 0
                        for i in range(len(products)):
                            if products[i].quantity < quantities[i]:
                                return Response({'error': 'The quantity of the product is not enough.'}, status=status.HTTP_400_BAD_REQUEST)
                            bill += products[i].price * quantities[i]
                        bill = bill * (100 - discount.discount) / 100
                        bill = bill * 1.1 # 10% tax
                        factor = Factor.objects.create(
                            user=request.user,
                            code=generate_unique_factor_code(),
                            total_price=bill,
                            discount=discount,
                        )
                        for i in range(len(products)):
                            FactorItem.objects.create(
                                factor=factor,
                                product=products[i],
                                quantity=quantities[i],
                                price = (products[i].price) * (100 - discount.discount) / 100,
                                total_price=(products[i].price * quantities[i]) * (100 - discount.discount) / 100,
                                discount = discount)
                            products[i].quantity -= quantities[i]
                            products[i].save()
                        return  Response({'message': 'The factor has been successfully created.'}, status=status.HTTP_201_CREATED)
                    

                elif discount.all_products and not discount.all_customers:
                    if request.user not in discount.user.all():
                        return Response({'error': 'You are not allowed to use this discount.'}, status=status.HTTP_400_BAD_REQUEST)
                    bill = 0
                    for i in range(len(products)):
                        if products[i].quantity < quantities[i]:
                            return Response({'error': 'The quantity of the product is not enough.'}, status=status.HTTP_400_BAD_REQUEST)
                        bill += products[i].price * quantities[i]
                    bill = bill * (100 - discount.discount) / 100
                    bill = bill * 1.1 # 10% tax
                    factor = Factor.objects.create(
                        user=request.user,
                        code=generate_unique_factor_code(),
                        total_price=bill,
                        discount=discount,
                    )
                    for i in range(len(products)):
                        FactorItem.objects.create(
                            factor=factor,
                            product=products[i],
                            quantity=quantities[i],
                            price = (products[i].price) * (100 - discount.discount) / 100,
                            total_price=(products[i].price * quantities[i]) * (100 - discount.discount) / 100,
                            discount = discount)
                        products[i].quantity -= quantities[i]
                        products[i].save()
                    return  Response({'message': 'The factor has been successfully created.'}, status=status.HTTP_201_CREATED)
                
                elif not discount.all_products and discount.all_customers:
                    bill = 0
                    flag = 0
                    for i in range(len(products)):
                        if products[i].quantity < quantities[i]:
                            return Response({'error': 'The quantity of the product is not enough.'}, status=status.HTTP_400_BAD_REQUEST)
                        if products[i] in discount.product.all():
                            bill += (products[i].price * quantities[i]) * (100 - discount.discount) / 100
                            flag = 1
                        else :
                            bill += products[i].price * quantities[i]
                    if flag == 0:
                        return Response({'error': 'this discount is not usable for your peoducts'}, status=status.HTTP_400_BAD_REQUEST)
                    bill = bill * 1.1 # 10% tax
                    factor = Factor.objects.create(
                        user=request.user,
                        code=generate_unique_factor_code(),
                        total_price=bill,
                        discount=discount,
                    )
                    for i in range(len(products)):
                        if products[i] in discount.product.all():
                            FactorItem.objects.create(
                                factor=factor,
                                product=products[i],
                                quantity=quantities[i],
                                price = (products[i].price) * (100 - discount.discount) / 100,
                                total_price=(products[i].price * quantities[i]) * (100 - discount.discount) / 100,
                                discount = discount)
                            products[i].quantity -= quantities[i]
                            products[i].save()
                        else :
                            FactorItem.objects.create(
                                factor=factor,
                                product=products[i],
                                quantity=quantities[i],
                                price = (products[i].price),
                                total_price=(products[i].price * quantities[i]))
                            products[i].quantity -= quantities[i]
                            products[i].save()
                    return  Response({'message': 'The factor has been successfully created.'}, status=status.HTTP_201_CREATED)
                elif not discount.all_products and not discount.all_customers:
                    if request.user not in discount.user.all():
                        return Response({'error': 'You are not allowed to use this discount.'}, status=status.HTTP_400_BAD_REQUEST)
                    bill = 0
                    flag = 0
                    for i in range(len(products)):
                        if products[i].quantity < quantities[i]:
                            return Response({'error': 'The quantity of the product is not enough.'}, status=status.HTTP_400_BAD_REQUEST)
                        if products[i] in discount.product.all():
                            bill += (products[i].price * quantities[i]) * (100 - discount.discount) / 100
                            flag = 1
                        else :
                            bill += products[i].price * quantities[i]
                    if flag == 0:
                        return Response({'error': 'this discount is not usable for your peoducts'}, status=status.HTTP_400_BAD_REQUEST)
                    bill = bill * 1.1 # 10% tax
                    factor = Factor.objects.create(
                        user=request.user,
                        code=generate_unique_factor_code(),
                        total_price=bill,
                        discount=discount,
                    )
                    for i in range(len(products)):
                        if products[i] in discount.product.all():
                            FactorItem.objects.create(
                                factor=factor,
                                product=products[i],
                                quantity=quantities[i],
                                price = (products[i].price) * (100 - discount.discount) / 100,
                                total_price=(products[i].price * quantities[i]) * (100 - discount.discount) / 100,
                                discount = discount)
                            products[i].quantity -= quantities[i]
                            products[i].save()
                        else :
                            FactorItem.objects.create(
                                factor=factor,
                                product=products[i],
                                quantity=quantities[i],
                                price = (products[i].price),
                                total_price=(products[i].price * quantities[i]))
                            products[i].quantity -= quantities[i]
                            products[i].save()
                    return  Response({'message': 'The factor has been successfully created.'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class FactorView(ListAPIView):
    permission_classes = [IsAuthenticated, IsSuperUser]

    queryset = Factor.objects.all()
    serializer_class = FactorViewSerilizer

from rest_framework.generics import RetrieveAPIView
class FactorRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsSuperUser]
    queryset = Factor.objects.all()
    serializer_class = FactorViewSerilizer





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

                
    
class TransactionList(ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['factor', 'type', 'created_at']
    ordering_fields = ['created_at']

