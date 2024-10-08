from django.db import models
from django.contrib.auth.models import User

class NaturalPerson(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    national_id = models.CharField(max_length=10)
    wallet = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class LegalPerson(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    company_address = models.TextField()
    company_id = models.CharField(max_length=10)
    is_active = models.BooleanField(default=False)
    wallet = models.DecimalField(max_digits=10, decimal_places=2, default=0)

