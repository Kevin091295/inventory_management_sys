from django import forms
from .models import Product, Category, Supplier, StockTransaction


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


class StockTransactionForm(forms.ModelForm):
    class Meta:
        model = StockTransaction
        fields = ['product', 'quantity', 'transaction_type', 'remarks'] 

    
    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        quantity = cleaned_data.get('quantity')
        transaction_type = cleaned_data.get('transaction_type')

        if transaction_type == 'REMOVE' and product and quantity:
            if product.stock_level < quantity:
                raise forms.ValidationError(f"Cannot remove {quantity} units. Only {product.stock_level} units available in inventory.")
        return cleaned_data