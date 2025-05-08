from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Reservation


def reservation(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        special_requirements = request.POST.get('special_requirements', '')
        guest_count = request.POST.get('guest_count')
        booking_date = request.POST.get('booking_date')
        booking_time = request.POST.get('booking_time')

         # Check for existing reservation (excluding special requirements)
        existing = Reservation.objects.filter(
            first_name=first_name,
            surname=surname,
            email=email,
            guest_count=guest_count,
            booking_date=booking_date,
            booking_time=booking_time
        ).exists()

        if existing:
            messages.error(request, f"A reservation already exists for {first_name} {surname} on {booking_date} at {booking_time}.")
        else:
            Reservation.objects.create(
                first_name=first_name,
                surname=surname,
                email=email,
                special_requirements=special_requirements,
                guest_count=guest_count,
                booking_date=booking_date,
                booking_time=booking_time,
            )
            messages.success(request, f"Thank you {first_name}, your table has been booked for {booking_date} at {booking_time}.")
            return redirect('reservation')
    return render(request, 'reservation/reservation.html')

@login_required
def view_reservations(request):
    reservations = Reservation.objects.all().order_by('booking_date', 'booking_time')
    return render(request, 'reservation/view_reservations.html', {'reservations': reservations})
