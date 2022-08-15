from django import forms
from .models import Manage_product

class Manage_productForm(forms.ModelForm):
    class Meta:
        model = Manage_product
        fields = ('product_name', 'description', 'image', 'price')