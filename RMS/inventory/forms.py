from django import forms
from .models import InventoryItem
from django.forms import ModelForm, TextInput, NumberInput, Select

class QuickOrderForm(forms.Form):
    """Form for placing a quick order."""
    item = forms.ModelChoiceField(
        queryset=InventoryItem.objects.all(),
        widget=Select(attrs={'class': 'form-control'}),
        label="Select Item"
    )
    quantity = forms.IntegerField(
        widget=NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'}),
        label="Order Quantity",
        min_value=1
    )
    supplier = forms.CharField(
        widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter supplier name'}),
        label="Supplier"
    )