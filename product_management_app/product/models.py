from django.db import models
from person.models import NaturalPerson, LegalPerson
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100)

class Product(models.Model):
    code = models.CharField(max_length=16)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    owner = models.ForeignKey(LegalPerson, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/')

class Discount(models.Model):
    product = models.ManyToManyField(Product, blank=True)
    User = models.ManyToManyField(User, blank=True)
    all_products = models.BooleanField(default=False)
    all_customers = models.BooleanField(default=False)
    code = models.CharField(max_length=9, unique=True)
    discount = models.PositiveBigIntegerField(validators=[MinValueValidator(1), MaxValueValidator(90)])
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.code

