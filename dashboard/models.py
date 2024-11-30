from django.db import models
from django.contrib.auth.models import User


from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, null=True
    )  # Link to Category
    stock_level = models.PositiveIntegerField(default=0)  # New field
    supplier = models.ForeignKey(
        "Supplier", on_delete=models.CASCADE, null=True
    )  # New field
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # New field

    def __str__(self):
        return f"{self.name}"


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.category_name


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name

from django.contrib.auth.models import User

class StockTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('ADD', 'Add Stock'),
        ('REMOVE', 'Remove Stock'),
    ]

    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, to_field="username")


    def __str__(self):
        return f'{self.transaction_type} - {self.product.name} ({self.quantity}) by {self.performed_by.username if self.performed_by else "Unknown"}'





class Order(models.Model):
    name = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"{self.customer}-{self.name}"
