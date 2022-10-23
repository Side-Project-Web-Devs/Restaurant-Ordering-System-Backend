from django import forms
from .models import Feedback, Inventory, Manage_product


class Manage_productForm(forms.ModelForm):
    class Meta:
        model = Manage_product
        fields = ('product_name', 'description', 'image', 'price')


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = ('feedback', 'reply')



