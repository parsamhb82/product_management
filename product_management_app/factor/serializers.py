from product.models import Discount
from rest_framework import serializers

from product.models import Discount, Product
from .models import *
class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'
    
    def create(self, validated_data):
        products = validated_data.pop('product', None)
        users = validated_data.pop('user', None)
        
        # Handle all products case
        if not products:
            validated_data['all_products'] = True
        else:
            validated_data['all_products'] = False

        # Handle all users case
        if not users:
            validated_data['all_customers'] = True
        else:
            validated_data['all_customers'] = False
        
        # Create the discount instance
        discount = Discount.objects.create(**validated_data)
        
        # Assign products if specific products were provided
        if products:
            discount.product.set(products)
        
        # Assign users if specific users were provided
        if users:
            discount.User.set(users)
        
        return discount
    
class ItemDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['factor', 'amount', 'type']

class FactorSerializer(serializers.Serializer):
    discount_code = serializers.CharField(max_length=9, required=False, allow_blank=True)
    products = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)
    quantities = serializers.ListField(
        child=serializers.IntegerField(min_value=1), 
        allow_empty=False
    )

    def validate(self, data):
        products = data.get('products')
        quantities = data.get('quantities')
        if len(products) != len(quantities):
            raise serializers.ValidationError("The number of products and quantities must match.")
        return data

class FactorItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactorItem
        fields = ['id', 'product', 'quantity', 'price', 'total_price', 'discount']

class FactorViewSerilizer(serializers.ModelSerializer):
    factor_items = FactorItemSerializer(many=True, source = 'factoritem_set')   

    class Meta:
        model = Factor
        fields = ['code', 'natural_person', 'discount', 'total_price', 'created_at', 'updated_at', 'is_paid', 'factor_items']



