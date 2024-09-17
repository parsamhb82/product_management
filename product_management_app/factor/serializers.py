from product.models import Discount
from rest_framework import serializers
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