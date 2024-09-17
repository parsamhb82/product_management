from rest_framework import viewsets
from .models import NaturalPerson, LegalPerson
from .serializers import NaturalPersonSerializer, LegalPersonSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
