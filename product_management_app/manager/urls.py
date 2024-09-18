from django.urls import path
from .views import (
    export_customers_csv, 
    export_products_csv, 
    export_factors_csv, 
    import_customers_csv, 
    import_products_csv, 
    import_factors_csv
)

urlpatterns = [
    path('export/customers/', export_customers_csv, name='export_customers_csv'),
    path('export/products/', export_products_csv, name='export_products_csv'),
    path('export/factors/', export_factors_csv, name='export_factors_csv'),
    
    path('import/customers/', import_customers_csv, name='import_customers_csv'),
    path('import/products/', import_products_csv, name='import_products_csv'),
    path('import/factors/', import_factors_csv, name='import_factors_csv'),
]
