from django import forms
from .models import Product, Order, Category, Supplier


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']
        widgets = {
            'category_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name'
            })
        }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'email', 'phone_number']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter supplier name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter supplier email'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
        }