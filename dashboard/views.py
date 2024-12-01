from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Product, StockTransaction, Category, Supplier
from .forms import ProductForm, CategoryForm, SupplierForm, StockTransactionForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import auth_users, allowed_users
from django.shortcuts import get_object_or_404

# Create your views here.


@login_required(login_url="user-login")
def index(request):

    stock_in_data = StockTransaction.objects.filter(transaction_type='IN').values('timestamp', 'quantity')
    stock_out_data = StockTransaction.objects.filter(transaction_type='OUT').values('timestamp', 'quantity')

    context = {
        'stock_in_data': list(stock_in_data),
        'stock_out_data': list(stock_out_data),
    }
    return render(request, 'dashboard/index.html', context)


@login_required(login_url="user-login")
def products(request):
    products = Product.objects.all()  # Fetch all products
    context = {
        "products": products,
    }
    return render(request, "dashboard/product_list.html", context)


@login_required(login_url="user-login")
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect("dashboard-products")
    else:
        form = ProductForm()

    context = {
        "form": form,
    }
    return render(request, "dashboard/add_product.html", context)


def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("dashboard-products")  # Redirect to the product list page
    else:
        form = ProductForm(instance=product)
    return render(
        request, "dashboard/edit_product.html", {"form": form, "product": product}
    )


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":  # Confirm delete
        product.delete()
        return redirect("dashboard-products")  # Redirect to the product list page
    return render(request, "dashboard/confirm_delete.html", {"object": product})


@login_required(login_url="user-login")
@allowed_users(allowed_roles=["Admin"])
def customers(request):
    customer = User.objects.filter(groups=2)
    customer_count = customer.count()
    product = Product.objects.all()
    product_count = product.count()
    context = {
        "customer": customer,
        "customer_count": customer_count,
        "product_count": product_count,
    }
    return render(request, "dashboard/customers.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=["Admin"])
def customer_detail(request, pk):
    customer = User.objects.filter(groups=2)
    customer_count = customer.count()
    product = Product.objects.all()
    product_count = product.count()
    customers = User.objects.get(id=pk)
    context = {
        "customers": customers,
        "customer_count": customer_count,
        "product_count": product_count,
    }
    return render(request, "dashboard/customers_detail.html", context)


@login_required
def stock_update_page(request):
    return render(request, "dashboard/update_stock.html")


@login_required(login_url="user-login")
@allowed_users(allowed_roles=["Admin", "Staff"])
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

    context = {
        "transactions": transactions,  # Pass transactions to the template
    }
    print("transactions", transactions)
    return render(request, "dashboard/stock_transaction_list.html", context)


def add_stock_transaction(request):
    if request.method == 'POST':
        form = StockTransactionForm(request.POST)
        if form.is_valid():
            # Save the form but don't commit yet
            transaction = form.save(commit=False)
            # Set the performed_by field to the logged-in user
            transaction.performed_by = request.user
            transaction.save()
            return redirect('dashboard-stock-transactions')  # Redirect to the transactions page
    else:
        form = StockTransactionForm()

    return render(request, 'dashboard/add_stock_transaction.html', {'form': form})


def edit_stock_transaction(request, pk):
    transaction = get_object_or_404(StockTransaction, pk=pk)
    if request.method == "POST":
        form = StockTransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('dashboard-stock-transactions')
    else:
        form = StockTransactionForm(instance=transaction)
    return render(request, 'dashboard/edit_stock_transaction.html', {'form': form})


@login_required(login_url="user-login")
def delete_stock_transaction(request, pk):
    transaction = get_object_or_404(StockTransaction, pk=pk)
    transaction.delete()
    messages.success(request, "Stock transaction deleted successfully!")
    return redirect('dashboard-stock-transactions')


@login_required(login_url="user-login")
def categories(request):
    categories = Category.objects.all()  # Fetch all categories
    context = {
        "categories": categories,
    }
    print("context", context)
    return render(request, "dashboard/category_list.html", context)


@login_required(login_url="user-login")
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully!")
            return redirect("dashboard-categories")  # Redirect back to categories list
    else:
        form = CategoryForm()

    context = {
        "form": form,
    }
    return render(request, "dashboard/add_category.html", context)


@login_required(login_url="user-login")
def edit_category(request, pk):
    category = get_object_or_404(Category, id=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully!")
            return redirect("dashboard-categories")
    else:
        form = CategoryForm(instance=category)

    context = {
        "form": form,
        "category": category,
    }
    return render(request, "dashboard/edit_category.html", context)


@login_required(login_url="user-login")
def delete_category(request, pk):
    category = get_object_or_404(Category, id=pk)
    category.delete()
    messages.success(request, "Category deleted successfully!")
    return redirect("dashboard-categories")


# View for listing suppliers
def suppliers(request):
    supplier_list = Supplier.objects.all()
    context = {"suppliers": supplier_list}
    return render(request, "dashboard/supplier_list.html", context)


# View for adding a supplier
def add_supplier(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        Supplier.objects.create(name=name, email=email, phone_number=phone_number)
        messages.success(request, "Supplier added successfully!")
        return redirect("dashboard-suppliers")
    return render(request, "dashboard/add_supplier.html")


# View for editing a supplier
def edit_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == "POST":
        supplier.name = request.POST.get("name")
        supplier.email = request.POST.get("email")
        supplier.phone_number = request.POST.get("phone_number")
        supplier.save()
        messages.success(request, "Supplier updated successfully!")
        return redirect("dashboard-suppliers")
    return render(request, "dashboard/edit_supplier.html", {"supplier": supplier})


# View for deleting a supplier
def delete_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    supplier.delete()
    messages.success(request, "Supplier deleted successfully!")
    return redirect("dashboard-suppliers")
