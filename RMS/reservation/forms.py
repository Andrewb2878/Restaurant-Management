from django import forms
from .models import Reservation

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

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        surname = cleaned_data.get('surname')
        email = cleaned_data.get('email')
        guest_count = cleaned_data.get('guest_count')
        booking_date = cleaned_data.get('booking_date')
        booking_time = cleaned_data.get('booking_time')

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
