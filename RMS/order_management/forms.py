from django import forms
from .models import Order, OrderItem
from core.models import MenuItem  

class OrderForm(forms.ModelForm):
    """Form for creating an order (without waiter selection)."""

    class Meta:
        model = Order
        fields = ['table_number', 'status']  # Removed waiter field

    table_number = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-2 bg-gray-700 rounded focus:outline-none focus:ring focus:border-yellow-500',
            'placeholder': 'Enter table number',
        })
    )

    status = forms.ChoiceField(
        choices=Order.STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 bg-gray-700 rounded focus:outline-none focus:ring focus:border-yellow-500',
        })
    )


class OrderItemForm(forms.ModelForm):
    """Form for adding items to an order."""

    class Meta:
        model = OrderItem
        fields = ['order', 'menu_item', 'quantity', 'notes']

    order = forms.ModelChoiceField(
        queryset=Order.objects.all(),
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 bg-gray-700 rounded focus:outline-none focus:ring focus:border-yellow-500',
        }),
        empty_label="Select an order"
    )

    menu_item = forms.ModelChoiceField(
        queryset=MenuItem.objects.all(),
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 bg-gray-700 rounded focus:outline-none focus:ring focus:border-yellow-500',
        }),
        empty_label="Select a menu item"
    )

    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-2 bg-gray-700 rounded focus:outline-none focus:ring focus:border-yellow-500',
            'placeholder': 'Enter quantity',
        })
    )

    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-2 bg-gray-700 rounded focus:outline-none focus:ring focus:border-yellow-500',
            'placeholder': 'Add special requests',
        })
    )