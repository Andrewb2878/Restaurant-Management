from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Reservation
from .forms import ReservationForm


def reservation(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            cd = form.cleaned_data
            messages.success(request, f"Thank you {cd['first_name']}, your table has been booked for {cd['booking_date']} at {cd['booking_time']}.")
            return redirect('reservation')
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = ReservationForm()

    return render(request, 'reservation/reservation.html', {'form': form})

@login_required
def view_reservations(request):
    reservations = Reservation.objects.all().order_by('booking_date', 'booking_time')
    return render(request, 'reservation/view_reservations.html', {'reservations': reservations})
