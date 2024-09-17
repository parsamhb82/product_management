from django.db import models
from django.contrib.auth.models import User
from person.models import NaturalPerson, LegalPerson
from product.models import Product, Discount
from django.utils import timezone




class Factor(models.Model):
    code = models.CharField(max_length=16, unique=True)
    natural_person = models.ForeignKey(NaturalPerson, on_delete=models.CASCADE, null=True, blank=True)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)
    paid_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def factor_discount(self):
        now =timezone.now()
        if self.discount and self.discount.start <= now <= self.discount.end:
            if self.discount.all_customers or self.discount.all_products:
                return self.discount.discount
            elif self.natural_person and self.discount.user.filter(id=self.natural_person.user.id).exists():
                return self.discount.discount
        return 0

    def __str__(self):
        return f"Factor {self.code}"
    

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
    TYPE_STATUS = (
        ("online", "online"),
        ("inperson", "inperson"),
    )
    code = models.CharField(max_length=16, unique=True)
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=TYPE_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.code