import csv
import random
import string
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .decorators import admin_required, auth_users, allowed_users, staff_or_admin
from .forms import ProductForm, CategoryForm, SupplierForm, StockTransactionForm
from .models import Product, StockTransaction, Category, Supplier


@login_required(login_url="user-login")
def dashboard_index(request):
    # Summary Cards Data
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_transactions = StockTransaction.objects.count()
    low_stock_items = Product.objects.filter(stock_level__lt=10).count()

    # Recent Transactions
    recent_transactions = StockTransaction.objects.order_by("-timestamp")[:5]

    # Stock Level Chart Data
    products = Product.objects.all()
    product_names = [product.name for product in products]
    product_stock_levels = [product.stock_level for product in products]
    stock_colors = [
        (
            "rgba(75, 192, 192, 0.7)"
            if product.stock_level >= 10
            else "rgba(255, 99, 132, 0.7)"
        )
        for product in products
    ]

    # Combine product names and stock levels
    stock_data = zip(product_names, product_stock_levels)

    context = {
        "total_products": total_products,
        "total_categories": total_categories,
        "total_transactions": total_transactions,
        "low_stock_items": low_stock_items,
        "recent_transactions": recent_transactions,
        "product_names": product_names,
        "product_stock_levels": product_stock_levels,
        "stock_colors": stock_colors,
        "stock_data": stock_data,  # Pass the combined data
    }
    return render(request, "dashboard/index.html", context)


# ------------------ PRODUCTS  ------------------
@login_required(login_url="user-login")
def products(request):
    products = Product.objects.all()  # Fetch all products
    context = {
        "products": products,
    }
    return render(request, "dashboard/product_list.html", context)


@login_required(login_url="user-login")
@admin_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(
                commit=False
            )  # Save the product without committing to the DB
            initial_stock = product.stock_level  # Get the initial stock level
            product.stock_level = 0  # Temporarily set stock level to 0 before saving
            product.save()  # Save the product to the database

            # Create an initial stock transaction if the stock level is greater than 0
            if initial_stock > 0:
                StockTransaction.objects.create(
                    product=product,
                    quantity=initial_stock,
                    transaction_type="ADD",
                    performed_by=request.user,
                    remarks=f"Initial stock for {product.name}",
                )

            messages.success(
                request,
                f"Product {product.name} added successfully with initial stock.",
            )
            return redirect("dashboard-products")
    else:
        form = ProductForm()

    return render(request, "dashboard/add_product.html", {"form": form})


@login_required(login_url="user-login")
@admin_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            updated_product = form.save(
                commit=False
            )  # Save the product data without committing to the DB
            old_stock_level = product.stock_level  # Retrieve the current stock level
            new_stock_level = (
                updated_product.stock_level
            )  # Retrieve the updated stock level

            # Save the product with the new stock level
            updated_product.save()

            # Determine the stock difference and create a transaction
            stock_difference = new_stock_level - old_stock_level
            if stock_difference != 0:
                transaction_type = "ADD" if stock_difference > 0 else "REMOVE"
                StockTransaction.objects.create(
                    product=updated_product,
                    quantity=abs(stock_difference),
                    transaction_type=transaction_type,
                    performed_by=request.user,
                    remarks=f"Stock level updated via product edit",
                )

            messages.success(request, f"Product {product.name} updated successfully.")
            return redirect("dashboard-products")
    else:
        form = ProductForm(instance=product)

    return render(
        request, "dashboard/edit_product.html", {"form": form, "product": product}
    )


@login_required
@admin_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        messages.success(request, f"Product {product.name} deleted successfully.")
        return redirect("dashboard-products")

    return render(request, "dashboard/confirm_delete.html", {"object": product})


# ------------------ PRODUCTS  ------------------
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


# ------------------ STOCK TRANSACTION  ------------------


@login_required(login_url="user-login")
@staff_or_admin
def stock_update(request):
    products = Product.objects.all()
    stock_transactions = StockTransaction.objects.all()
    product_count = products.count()
    transaction_count = stock_transactions.count()

    if request.method == "POST":
        product_id = request.POST.get("product")
        transaction_type = request.POST.get("transaction_type")
        quantity = int(request.POST.get("quantity"))
        product = get_object_or_404(Product, id=product_id)

        if transaction_type == "REMOVE":
            if product.stock_level >= quantity:
                product.stock_level -= quantity
            else:
                messages.error(request, "Insufficient stock!")
                return redirect("dashboard-stock-update")
        elif transaction_type == "ADD":
            product.stock_level += quantity

        # Save product and transaction
        product.save()
        StockTransaction.objects.create(
            product=product,
            quantity=quantity,
            transaction_type=transaction_type,
            performed_by=request.user,
        )
        messages.success(
            request,
            f"Stock successfully updated: {transaction_type.lower()} {quantity} units of {product.name}.",
        )
        return redirect("dashboard-stock-update")

    context = {
        "products": products,
        "product_count": product_count,
        "transaction_count": transaction_count,
    }
    return render(request, "dashboard/stock_update.html", context)


@login_required(login_url="user-login")
def stock_transaction_list(request):
    transactions = StockTransaction.objects.all().order_by("-timestamp")

    # Get filter values from the request
    transaction_type = request.GET.get("transaction_type", "")
    product_id = request.GET.get("product", "")
    performed_by = request.GET.get("performed_by", "")
    date_from = request.GET.get("date_from", "")
    date_to = request.GET.get("date_to", "")
    search_query = request.GET.get("search_query", "")

    # Apply filters
    if transaction_type:
        transactions = transactions.filter(transaction_type=transaction_type)

    if product_id:
        transactions = transactions.filter(product__id=product_id)

    if performed_by:
        transactions = transactions.filter(performed_by__username=performed_by)

    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, "%Y-%m-%d")
            transactions = transactions.filter(timestamp__date__gte=date_from_obj)
        except ValueError:
            pass

    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, "%Y-%m-%d")
            transactions = transactions.filter(timestamp__date__lte=date_to_obj)
        except ValueError:
            pass

    if search_query:
        transactions = transactions.filter(reference_number__icontains=search_query)

    # Fetch necessary data for filters
    products = Product.objects.all()
    users = User.objects.values_list("username", flat=True)
    transaction_types = StockTransaction.TRANSACTION_TYPES

    context = {
        "transactions": transactions,
        "products": products,
        "users": users,
        "transaction_types": transaction_types,
        "transaction_type": transaction_type,
        "product_id": product_id,
        "performed_by": performed_by,
        "date_from": date_from,
        "date_to": date_to,
        "search_query": search_query,
    }

    return render(request, "dashboard/stock_transaction_list.html", context)


def get_stock_level(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        return JsonResponse({"stock_level": product.stock_level})
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)


@login_required
def add_stock_transaction(request):
    if request.method == "POST":
        form = StockTransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.performed_by = request.user
            transaction.save()
            messages.success(
                request,
                f"Successfully added stock transaction for {transaction.product.name}.",
            )
            return redirect("dashboard-stock-transactions")
        else:
            messages.error(
                request, "Failed to add stock transaction. Please check the form."
            )
    else:
        form = StockTransactionForm()

    return render(request, "dashboard/add_stock_transaction.html", {"form": form})


def edit_stock_transaction(request, pk):
    transaction = get_object_or_404(StockTransaction, pk=pk)
    if request.method == "POST":
        form = StockTransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect("dashboard-stock-transactions")
    else:
        form = StockTransactionForm(instance=transaction)
    return render(request, "dashboard/edit_stock_transaction.html", {"form": form})


@login_required
def delete_stock_transaction(request, pk):
    transaction = get_object_or_404(StockTransaction, pk=pk)
    product_name = transaction.product.name
    transaction.delete()
    messages.success(
        request, f"Stock transaction for {product_name} was successfully deleted."
    )
    return redirect("dashboard-stock-transactions")


def low_stock_items(request):
    low_stock_products = Product.objects.filter(stock_level__lt=10)
    return render(
        request,
        "dashboard/low_stock_items.html",
        {"low_stock_products": low_stock_products},
    )


# ------------------ CATEGORY  ------------------
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


@login_required(login_url="user-login")
def categories(request):
    categories = Category.objects.all()  # Fetch all categories
    context = {
        "categories": categories,
    }

    return render(request, "dashboard/category_list.html", context)


@login_required
@admin_required
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully.")
            return redirect("dashboard-categories")
        else:
            messages.error(request, "Failed to add category. Please try again.")
    else:
        form = CategoryForm()
    return render(request, "dashboard/add_category.html", {"form": form})


@login_required
@admin_required
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully.")
            return redirect("dashboard-categories")
    else:
        form = CategoryForm(instance=category)
    return render(request, "dashboard/edit_category.html", {"form": form})


@login_required(login_url="user-login")
@admin_required
def delete_category(request, pk):
    category = get_object_or_404(Category, id=pk)
    category.delete()
    messages.success(request, "Category deleted successfully!")
    return redirect("dashboard-categories")


# ------------------ SUPPLIER  ------------------
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


def suppliers(request):
    supplier_list = Supplier.objects.all()
    context = {"suppliers": supplier_list}
    return render(request, "dashboard/supplier_list.html", context)


@login_required
@admin_required
def add_supplier(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Supplier added successfully.")
            return redirect("dashboard-suppliers")
        else:
            messages.error(request, "Failed to add supplier. Please try again.")
    else:
        form = SupplierForm()
    return render(request, "dashboard/add_supplier.html", {"form": form})


@login_required
@admin_required
def edit_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == "POST":
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, "Supplier updated successfully.")
            return redirect("dashboard-suppliers")
    else:
        form = SupplierForm(instance=supplier)
    return render(request, "dashboard/edit_supplier.html", {"form": form})


# View for deleting a supplier
@admin_required
def delete_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    supplier.delete()
    messages.success(request, "Supplier deleted successfully!")
    return redirect("dashboard-suppliers")


@login_required
def export_products(request):
    # Create the HttpResponse object with CSV headers
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'

    writer = csv.writer(response)
    # Write the header row
    writer.writerow(['Product Name', 'Category', 'Supplier', 'Stock Level', 'Price'])

    # Write the product rows
    for product in Product.objects.all():
        writer.writerow([product.name, product.category.category_name, product.supplier.name, product.stock_level, product.price])

    return response


@login_required
def export_transactions(request):
    # Get filtered transactions
    transactions = StockTransaction.objects.all()

    # Apply filters (same as in the stock_transaction_list view)
    transaction_type = request.GET.get("transaction_type", "")
    product_id = request.GET.get("product", "")
    performed_by = request.GET.get("performed_by", "")
    date_from = request.GET.get("date_from", "")
    date_to = request.GET.get("date_to", "")

    if transaction_type:
        transactions = transactions.filter(transaction_type=transaction_type)
    if product_id:
        transactions = transactions.filter(product__id=product_id)
    if performed_by:
        transactions = transactions.filter(performed_by__username=performed_by)
    if date_from:
        transactions = transactions.filter(timestamp__date__gte=date_from)
    if date_to:
        transactions = transactions.filter(timestamp__date__lte=date_to)

    # Create the HttpResponse object with CSV headers
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'

    writer = csv.writer(response)
    # Write the header row
    writer.writerow(['Reference Number', 'Product', 'Transaction Type', 'Quantity', 'Performed By', 'Date', 'Remarks'])

    # Write the transaction rows
    for transaction in transactions:
        writer.writerow([
            transaction.reference_number,
            transaction.product.name,
            transaction.get_transaction_type_display(),
            transaction.quantity,
            transaction.performed_by.username if transaction.performed_by else "Unknown",
            transaction.timestamp.strftime("%Y-%m-%d"),
            transaction.remarks or ""
        ])

    return response

