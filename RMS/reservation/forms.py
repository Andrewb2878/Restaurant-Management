from django import forms
from .models import Reservation
from django.core.mail import send_mail

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            'first_name',
            'surname',
            'email',
            'special_requirements',
            'guest_count',
            'booking_date',
            'booking_time',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Check if there's a period after the @ symbol
        if '@' in email:
            domain_part = email.split('@')[1]
        
            # Ensure there's a period (.) in the domain part
            if '.' not in domain_part:
                raise forms.ValidationError('The provided email address is invalid.')
        
            # Check that the domain part is long enough (minimum 2 characters)
            domain_without_extension = domain_part.split('.')[0]
            if len(domain_without_extension) < 2:
                raise forms.ValidationError('The provided email address is invalid.')
        else:
            raise forms.ValidationError('The provided email address is invalid.')

        return email


    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        surname = cleaned_data.get('surname')
        email = cleaned_data.get('email')
        guest_count = cleaned_data.get('guest_count')
        booking_date = cleaned_data.get('booking_date')
        booking_time = cleaned_data.get('booking_time').strftime('%H:%M')

        if Reservation.objects.filter(
            first_name=first_name,
            surname=surname,
            email=email,
            guest_count=guest_count,
            booking_date=booking_date,
            booking_time=booking_time
        ).exists():
            raise forms.ValidationError(
                f"A reservation already exists for {first_name} {surname} on {booking_date} at {booking_time}."
            )

        return cleaned_data

    # Sending confirmation email
    def send_confirmation_email(self):
        formatted_time = self.cleaned_data['booking_time'].strftime('%H:%M')
    
        send_mail(
            subject='Your Reservation Confirmation',
            message=(
                f"Dear {self.cleaned_data['first_name']},\n\n"
                f"Thank you for your reservation at MUTLULUK.\n"
                f"Here are your booking details:\n"
                f"Date: {self.cleaned_data['booking_date']}\nTime: {self.cleaned_data['booking_time']}\nGuests: {self.cleaned_data['guest_count']}\n\n"
                f"We look forward to seeing you!\n\nMUTLULUK Team"
            ),
            from_email=None,  # uses DEFAULT_FROM_EMAIL
            recipient_list=[self.cleaned_data['email']],
            fail_silently=False,
        )
