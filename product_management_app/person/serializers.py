from rest_framework import serializers
from .models import NaturalPerson, LegalPerson

class NaturalPersonSerializer:
    class Meta:
        model = NaturalPerson
        fields = ['id', 'user', 'national_id', 'wallet']

class LegalPersonSerializer:
    class Meta:
        model = LegalPerson
        fields = ['id', 'user', 'company_name', 'company_address', 'company_id', 'is_active', 'wallet']
                