from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import NaturalPerson, LegalPerson
from .serializers import NaturalPersonSerializer, LegalPersonSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
class NaturalPersonListCreateView(ListCreateAPIView):
    queryset = NaturalPerson.objects.all()
    serializer_class = NaturalPersonSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['wallet']
    search_fields = ['national_id', 'user__username']

class  NaturalPersonRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = NaturalPerson.objects.all()
    serializer_class = NaturalPersonSerializer
    
class LegalPersonListCreateView(ListCreateAPIView):
    queryset = LegalPerson.objects.all()
    serializer_class = LegalPersonSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active', 'wallet']
    search_fields = ['company_name', 'company_id', 'user__username']

class LegalPersonRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = LegalPerson.objects.all()
    serializer_class = LegalPersonSerializer