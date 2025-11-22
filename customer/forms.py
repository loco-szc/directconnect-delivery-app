from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['location', 'destination', 'is_perishable', 'weight', 'description']
        widgets = {
            'location': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Pickup Location'
            }),
            'destination': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Delivery Destination'
            }),
            'is_perishable': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Weight in kg'
            }),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Describe the content of your cargo'
            }),
        }
