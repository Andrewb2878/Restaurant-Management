# core/forms.py
from django import forms
from .models import Feedback
from django.contrib.auth.forms import AuthenticationForm


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'subject', 'message']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if '@' in email:
            domain_part = email.split('@')[1]
        
            # Ensure there's a period (.) in the domain part
            if '.' not in domain_part:
                raise forms.ValidationError('The provided email address is invalid. A domain name must include a dot.')
            
            # Check that the domain part is long enough (e.g., "gmail" is fine, "g" is not)
            domain_without_extension = domain_part.split('.')[0]
            if len(domain_without_extension) < 2:
                raise forms.ValidationError('The domain name is too short to be valid.')
        else:
            raise forms.ValidationError('The email must contain an "@" symbol.')

        return email

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
