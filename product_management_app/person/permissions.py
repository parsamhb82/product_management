from rest_framework.permissions import BasePermission
from .models import NaturalPerson, LegalPerson
from django.contrib.auth.models import User

class IsNaturalUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            try:
                natural_person = NaturalPerson.objects.get(user=user)
                return True
            except NaturalPerson.DoesNotExist:
                return False
        return False

class IsLegalUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            try:
                legal_person = LegalPerson.objects.get(user=user)
                return True
            except LegalPerson.DoesNotExist:
                return False
        return False