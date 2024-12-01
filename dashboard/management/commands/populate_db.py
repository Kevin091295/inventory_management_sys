import random
import uuid
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from dashboard.models import Category, Supplier, Product, StockTransaction
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Populate the database with dummy data'

    def handle(self, *args, **kwargs):
        # Step 1: Create Categories
        categories = [
            "Beverages", "Snacks", "Dairy", "Frozen Foods", "Bakery", 
            "Personal Care", "Household Supplies", "Fruits", "Vegetables", "Confectionery"
        ]
        category_objects = []
        for category_name in categories:
            category, created = Category.objects.get_or_create(category_name=category_name)
            category_objects.append(category)
        self.stdout.write(self.style.SUCCESS(f"Created {len(category_objects)} categories"))

        # Step 2: Create Suppliers
        suppliers = [
            {"name": "Morning Glory Supplies", "email": "contact@morningglory.com", "phone_number": "1234567890"},
            {"name": "Swift Beverages", "email": "sales@swiftbeverages.com", "phone_number": "9876543210"},
            {"name": "Fresh Produce Co.", "email": "support@freshproduce.com", "phone_number": "5556667777"},
            {"name": "SnackWorld", "email": "hello@snackworld.com", "phone_number": "1112223333"},
            {"name": "Pure Dairy", "email": "info@puredairy.com", "phone_number": "4445556666"},
            {"name": "Frozen Delights", "email": "orders@frozendelights.com", "phone_number": "7778889999"},
            {"name": "Household Hub", "email": "service@householdhub.com", "phone_number": "2223334444"},
            {"name": "BakeCraft", "email": "bakecraft@bakery.com", "phone_number": "9998887776"},
            {"name": "FruitFarm", "email": "support@fruitfarm.com", "phone_number": "6665554443"},
            {"name": "SweetTooth Confectionery", "email": "info@sweettooth.com", "phone_number": "3332221110"}
        ]
        supplier_objects = []
        for supplier_data in suppliers:
            supplier, created = Supplier.objects.get_or_create(
                name=supplier_data["name"], 
                email=supplier_data["email"], 
                phone_number=supplier_data["phone_number"]
            )
            supplier_objects.append(supplier)
        self.stdout.write(self.style.SUCCESS(f"Created {len(supplier_objects)} suppliers"))

        # Step 3: Create Products
        product_names = [
            "Coke", "Pepsi", "Milk", "Cheese", "Frozen Pizza", "Bread", 
            "Toothpaste", "Detergent", "Apples", "Bananas", "Chips", "Cookies",
            "Yogurt", "Butter", "Ice Cream", "Cake", "Tomatoes", "Carrots",
            "Candy", "Chocolates"
        ]
        product_objects = []
        for product_name in product_names:
            product = Product.objects.create(
                name=product_name,
                category=random.choice(category_objects),
                supplier=random.choice(supplier_objects),
                stock_level=random.randint(10, 100),
                price=random.uniform(1.0, 20.0)
            )
            product_objects.append(product)
        self.stdout.write(self.style.SUCCESS(f"Created {len(product_objects)} products"))

        # Step 4: Create Stock Transactions
        transaction_types = ["ADD", "REMOVE"]
        admin_user = User.objects.get_or_create(username="admin", is_superuser=True)[0]
        kevin_user = User.objects.get_or_create(username="kevin", is_staff=True)[0]
        users = [admin_user, kevin_user]
        stock_transactions = []
        for _ in range(70):  # Create 70 transactions
            product = random.choice(product_objects)
            transaction_type = random.choice(transaction_types)
            quantity = random.randint(1, 20)
            performed_by = random.choice(users)
            reference_number = f"TRX-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4()}"
            remarks = f"Dummy transaction for {product.name}"
            transaction = StockTransaction.objects.create(
                product=product,
                quantity=quantity,
                transaction_type=transaction_type,
                performed_by=performed_by,
                reference_number=reference_number,
                remarks=remarks
            )
            stock_transactions.append(transaction)
        self.stdout.write(self.style.SUCCESS(f"Created {len(stock_transactions)} stock transactions"))
