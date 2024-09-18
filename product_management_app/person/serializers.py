from rest_framework import serializers
from .models import NaturalPerson, LegalPerson
from django.contrib.auth.models import User

class NaturalPersonSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = NaturalPerson
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'national_id', 'wallet']

class LegalPersonSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')
    class Meta:
        model = LegalPerson
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'company_name', 'company_address', 'company_id', 'is_active', 'wallet']


class NaturalPersonRegisterSerializer(serializers.ModelSerializer):
    national_id = serializers.CharField(max_length=10)
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'national_id']
        extra_kwargs = {'password': {'write_only': True}}

class LegalPersonRegisterSerializer(serializers.ModelSerializer):
    company_id = serializers.CharField(max_length=10)
    company_address = serializers.CharField()
    company_name = serializers.CharField(max_length=100)
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'company_id', 'company_address', 'company_name']
        extra_kwargs = {'password': {'write_only': True}}



                