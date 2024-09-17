from django.urls import path
from .views import (
    NaturalPersonListCreateView,
    NaturalPersonRetrieveUpdateDestroyView,
    LegalPersonListCreateView,
    LegalPersonRetrieveUpdateDestroyView
)

urlpatterns = [
    path('natural_persons/', NaturalPersonListCreateView.as_view(), name='natural-person-list-create'),
    path('natural_persons/<int:pk>/', NaturalPersonRetrieveUpdateDestroyView.as_view(), name='natural-person-detail'),
    path('legal_persons/', LegalPersonListCreateView.as_view(), name='legal-person-list-create'),
    path('legal_persons/<int:pk>/', LegalPersonRetrieveUpdateDestroyView.as_view(), name='legal-person-detail'),
]
