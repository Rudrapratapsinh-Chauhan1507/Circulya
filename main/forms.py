from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # Only include fields that exist in your model
        fields = ['title', 'description', 'price', 'image']
