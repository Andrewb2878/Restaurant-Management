# core/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class PortalLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Optionally customize field widgets
        self.fields['username'].widget.attrs.update({
            'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-lg focus:ring-blue-500 focus:outline-none text-black',
            'placeholder': 'Username'
        })

        self.fields['password'].widget.attrs.update({
            'class': 'mt-1 block w-full px-4 py-2 pr-10 border border-gray-300 rounded-md shadow-lg focus:ring-blue-500 focus:outline-none text-black',
            'placeholder': 'Password'
        })
