from django.contrib import admin
from .models import *
@admin.register (Product)
class ProductAdmin(admin.ModelAdmin): ...


@admin.register (Discount)
class DiscounttAdmin(admin.ModelAdmin): ...

@admin.register (Category)
class ProductAdmin(admin.ModelAdmin): ...
# Register your models here.
