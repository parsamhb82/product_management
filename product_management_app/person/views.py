from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from .models import NaturalPerson, LegalPerson
from .serializers import *
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsNaturalUser, IsLegalUser
from factor.permission import IsSuperUser
class NaturalPersonListView(ListAPIView):

    permission_classes = [IsSuperUser]
    queryset = NaturalPerson.objects.all()
    serializer_class = NaturalPersonSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['wallet']
    search_fields = ['national_id', 'user__username']


class DestroyNaturalPersonView(DestroyAPIView):
    permission_classes = [IsSuperUser]
    queryset = NaturalPerson.objects.all()
    serializer_class = NaturalPersonSerializer

class NaturalPersonRetrieveView(RetrieveAPIView):
    permission_classes = [IsSuperUser]
    queryset = NaturalPerson.objects.all()
    serializer_class = NaturalPersonSerializer

class NaturalPersonUpdateView(UpdateAPIView):

    permission_classes = [IsNaturalUser | IsSuperUser]
    queryset = NaturalPerson.objects.all()
    serializer_class = NaturalPersonSerializer
    def get_queryset(self):
        return NaturalPerson.objects.filter(user=self.request.user)
    
class LegalPersonListView(ListAPIView):
    permission_classes = [IsSuperUser]
    queryset = LegalPerson.objects.all()
    serializer_class = LegalPersonSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active', 'wallet']
    search_fields = ['company_name', 'company_id', 'username']

class LegalPersonRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = LegalPerson.objects.all()
    serializer_class = LegalPersonSerializer

class LegalPersonRetrieveView(RetrieveAPIView):
    permission_classes = [IsSuperUser]
    queryset = LegalPerson.objects.all()
    serializer_class = LegalPersonSerializer

class LegalPersonUpdateView(UpdateAPIView):
    permission_classes = [IsLegalUser]
    queryset = LegalPerson.objects.all()
    serializer_class = LegalPersonSerializer
    def get_queryset(self):
        return LegalPerson.objects.filter(user=self.request.user)

class LegalPersonDestroyView(DestroyAPIView):
    permission_classes = [IsSuperUser]
    queryset = LegalPerson.objects.all()
    serializer_class = LegalPersonSerializer

class NaturalPersonCreateView(CreateAPIView):
    queryset = NaturalPerson.objects.all()
    serializer_class = NaturalPersonRegisterSerializer

    def perform_create(self, serializer):
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
            email=serializer.validated_data['email'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name']
        )
        NaturalPerson.objects.create(user=user, national_id=serializer.validated_data['national_id'])

class LegalPersonCreateView(CreateAPIView):
    queryset = LegalPerson.objects.all()
    serializer_class = LegalPersonRegisterSerializer

    def perform_create(self, serializer):
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
            email=serializer.validated_data['email'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name']
        )
        LegalPerson.objects.create(user=user, company_name=serializer.validated_data['company_name'], company_address=serializer.validated_data['company_address'], company_id=serializer.validated_data['company_id'])
