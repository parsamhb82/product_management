from django.urls import path
from .views import (
    ExportCustomersCSV,
    ExportProductsCSV,
    ExportFactorsCSV,
    ImportCustomersCSV,
    ImportProductsCSV,
    ImportFactorsCSV,
)

urlpatterns = [
    path("export/customers/", ExportCustomersCSV.as_view(), name="export_customers_csv"),
    path("export/products/", ExportProductsCSV.as_view(), name="export_products_csv"),
    path("export/factors/", ExportFactorsCSV.as_view(), name="export_factors_csv"),
    path("import/customers/", ImportCustomersCSV.as_view(), name="import_customers_csv"),
    path("import/products/", ImportProductsCSV.as_view(), name="import_products_csv"),
    path("import/factors/", ImportFactorsCSV.as_view(), name="import_factors_csv"),
]
