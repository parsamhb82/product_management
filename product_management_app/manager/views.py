import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import NaturalPerson, LegalPerson, Product, Factor


def export_customers_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="customers.csv"'

    writer = csv.writer(response)

    writer.writerow(["Username", "National ID", "Wallet"])
    natural_customers = NaturalPerson.objects.all()
    for customer in natural_customers:
        writer.writerow([customer.user.username, customer.national_id, customer.wallet])

    writer.writerow(
        ["Username", "Company Name", "Company Address", "Company ID", "Wallet"]
    )
    legal_customers = LegalPerson.objects.all()
    for customer in legal_customers:
        writer.writerow(
            [
                customer.user.username,
                customer.company_name,
                customer.company_address,
                customer.company_id,
                customer.wallet,
            ]
        )

    return response


def export_products_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="products.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ["Code", "Name", "Description", "Price", "Category", "Owner", "Stock"]
    )

    products = Product.objects.all()
    for product in products:
        writer.writerow(
            [
                product.code,
                product.name,
                product.description,
                product.price,
                product.category.name,
                product.owner.company_name,
                product.stock,
            ]
        )

    return response


def export_factors_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="factors.csv"'

    writer = csv.writer(response)
    writer.writerow(["Code", "Natural Person", "Total Price", "Created At", "Paid"])

    factors = Factor.objects.all()
    for factor in factors:
        writer.writerow(
            [
                factor.code,
                factor.natural_person.user.username if factor.natural_person else "",
                factor.total_price,
                factor.created_at,
                factor.is_paid,
            ]
        )

    return response


def import_customers_csv(request):
    if request.method == "POST":
        csv_file = request.FILES["file"]
        decoded_file = csv_file.read().decode("utf-8").splitlines()
        reader = csv.reader(decoded_file)
        next(reader)

        for row in reader:
            user_name = row[0]
            national_id = row[1]
            wallet = row[2]

            user, created = User.objects.get_or_create(username=user_name)

            NaturalPerson.objects.update_or_create(
                user=user,
                defaults={
                    "national_id": national_id,
                    "wallet": wallet,
                },
            )

        return redirect("some_success_url")

    return render(request, "import_csv.html")


def import_products_csv(request):
    if request.method == "POST":
        csv_file = request.FILES["file"]
        decoded_file = csv_file.read().decode("utf-8").splitlines()
        reader = csv.reader(decoded_file)
        next(reader)

        for row in reader:
            code = row[0]
            name = row[1]
            description = row[2]
            price = row[3]
            stock = row[4]

            Product.objects.update_or_create(
                code=code,
                defaults={
                    "name": name,
                    "description": description,
                    "price": price,
                    "stock": stock,
                },
            )

        return redirect("some_success_url")

    return render(request, "import_csv.html")


def import_factors_csv(request):
    if request.method == "POST":
        csv_file = request.FILES["file"]
        decoded_file = csv_file.read().decode("utf-8").splitlines()
        reader = csv.reader(decoded_file)
        next(reader)

        for row in reader:
            code = row[0]
            total_price = row[1]
            is_paid = row[2]

            Factor.objects.update_or_create(
                code=code,
                defaults={
                    "total_price": total_price,
                    "is_paid": is_paid,
                },
            )

        return redirect("some_success_url")

    return render(request, "import_csv.html")
