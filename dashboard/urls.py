from django.urls import path
from . import views
from .models import Product, Supplier, Category

urlpatterns = [
    path('index/', views.index, name='dashboard-index'),

    
    path('products/', views.products, name='dashboard-products'),  # Product list
    path('products/add/', views.add_product, name='add-product'),  # Add product

    path('products/delete/<int:pk>/', views.product_delete,
         name='dashboard-products-delete'),
    path('products/detail/<int:pk>/', views.product_detail,
         name='dashboard-products-detail'),
    path('products/edit/<int:pk>/', views.product_edit,
         name='dashboard-products-edit'),
    path('customers/', views.customers, name='dashboard-customers'),
    path('customers/detial/<int:pk>/', views.customer_detail,
         name='dashboard-customer-detail'),
    path('order/', views.order, name='dashboard-order'),


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
    path('update_stock_page/', views.stock_update_page, name='stock_update_page'),
    path('update_stock/<int:product_id>/<int:quantity>/<str:transaction_type>/', views.stock_update, name='update_stock'),

]
