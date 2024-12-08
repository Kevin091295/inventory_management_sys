import os
import django
import random
import string

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management_system.settings')
django.setup()

from django.contrib.auth.models import User
from dashboard.models import Product, Category, Supplier, StockTransaction


def populate_categories():
    categories = ["Beverages", "Snacks", "Dairy", "Frozen Foods", "Personal Care"]
    for category_name in categories:
        Category.objects.get_or_create(category_name=category_name)
    print("Categories added successfully!")


def populate_suppliers():
    suppliers = [
        {"name": "Morning Glory Supplies", "email": "info@morningglory.com", "phone_number": "123-456-7890"},
        {"name": "Swift Beverages", "email": "contact@swiftbeverages.com", "phone_number": "321-654-0987"},
        {"name": "Pure Dairy Suppliers", "email": "sales@puredairy.com", "phone_number": "987-654-3210"},
    ]
    for supplier_data in suppliers:
        Supplier.objects.get_or_create(**supplier_data)
    print("Suppliers added successfully!")


def populate_products():
    category_beverages = Category.objects.get(category_name="Beverages")
    category_snacks = Category.objects.get(category_name="Snacks")
    supplier_glory = Supplier.objects.get(name="Morning Glory Supplies")
    supplier_swift = Supplier.objects.get(name="Swift Beverages")

    products = [
        {"name": "Coke", "category": category_beverages, "supplier": supplier_swift, "stock_level": 50, "price": 1.50},
        {"name": "Pepsi", "category": category_beverages, "supplier": supplier_swift, "stock_level": 40, "price": 1.45},
        {"name": "Cheese", "category": category_snacks, "supplier": supplier_glory, "stock_level": 30, "price": 2.75},
        {"name": "Chips", "category": category_snacks, "supplier": supplier_glory, "stock_level": 20, "price": 1.25},
    ]

    for product_data in products:
        Product.objects.get_or_create(**product_data)
    print("Products added successfully!")


def populate_stock_transactions():
    products = Product.objects.all()
    admin_user = User.objects.filter(is_superuser=True).first()

    if not admin_user:
        print("No superuser found. Please create an admin user first.")
        return

    transactions = [
        {"product": "Coke", "quantity": 10, "transaction_type": "ADD", "remarks": "Initial stock"},
        {"product": "Pepsi", "quantity": 15, "transaction_type": "ADD", "remarks": "New stock delivery"},
        {"product": "Cheese", "quantity": 5, "transaction_type": "REMOVE", "remarks": "Customer purchase"},
        {"product": "Chips", "quantity": 20, "transaction_type": "REMOVE", "remarks": "Bulk sale"},
    ]

    for transaction in transactions:
        product = Product.objects.get(name=transaction["product"])
        stock_transaction = StockTransaction(
            product=product,
            quantity=transaction["quantity"],
            transaction_type=transaction["transaction_type"],
            performed_by=admin_user,
            remarks=transaction["remarks"],
        )
        # Call save to trigger unique reference_number generation
        stock_transaction.save()

    print("Stock transactions added successfully!")


def create_admin_user():
    username = "admin"
    password = "admin123"
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, password=password, email="admin@example.com")
        print(f"Superuser '{username}' created with password '{password}'")
    else:
        print(f"Superuser '{username}' already exists.")


def main():
    print("Populating the database...")

    create_admin_user()
    populate_categories()
    populate_suppliers()
    populate_products()
    populate_stock_transactions()

    print("Database populated successfully!")


if __name__ == "__main__":
    main()
