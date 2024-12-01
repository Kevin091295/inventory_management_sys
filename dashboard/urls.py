from django.urls import path
from . import views
from .models import Product, Supplier, Category

urlpatterns = [
    path('index/', views.index, name='dashboard-index'),

    path('customers/', views.customers, name='dashboard-customers'),
    path('customers/detial/<int:pk>/', views.customer_detail,
         name='dashboard-customer-detail'),

    # Products
    path('products/', views.products, name='dashboard-products'),  # Product list
    path('products/add/', views.add_product, name='add-product'),  # Add product
    path('products/edit/<int:pk>/', views.edit_product, name='edit-product'),
    path('products/delete/<int:pk>/', views.delete_product, name='delete-product'),

    # Categories
    path('categories/', views.categories, name='dashboard-categories'),  # Category list
    path('categories/add/', views.add_category, name='add-category'),  # Add category
    path('categories/edit/<int:pk>/', views.edit_category, name='edit-category'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete-category'),

    # Suppliers
    path('suppliers/', views.suppliers, name='dashboard-suppliers'),  # Supplier list
    path('suppliers/add/', views.add_supplier, name='add-supplier'),  # Add supplier
    path('suppliers/edit/<int:pk>/', views.edit_supplier, name='edit-supplier'),
    path('suppliers/delete/<int:pk>/', views.delete_supplier, name='delete-supplier'),

    # stock transactions
    path('stock-transactions/', views.stock_transaction_list, name='dashboard-stock-transactions'),
    path('get-stock-level/<int:product_id>/', views.get_stock_level, name='get-stock-level'),
    path('stock-transactions/add/', views.add_stock_transaction, name='add-stock-transaction'),
    path('stock-transactions/edit/<int:pk>/', views.edit_stock_transaction, name='edit-stock-transaction'),
    path('stock-transactions/delete/<int:pk>/', views.delete_stock_transaction, name='delete-stock-transaction'),
]
