from django.db import models
from django.contrib.auth.models import User
from person.models import NaturalPerson, LegalPerson
from product.models import Product, Discount

class Factor(models.Model):
    code = models.CharField(max_length=16, unique=True)
    NaturalPerson = models.ForeignKey(NaturalPerson, on_delete=models.CASCADE)
    legal_person = models.ForeignKey(LegalPerson, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.code

class FactorItem(models.Model):
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return f"{self.factor.code}, {self.product.name}, {self.quantity}"

class Transaction(models.Model):
    code = models.CharField(max_length=16, unique=True)
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.code