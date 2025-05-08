from django.shortcuts import render, redirect
from .models import Reservation

def reservation(request):
    if request.method == "POST":
        Reservation.objects.create(
            first_name=request.POST['first_name'],
            surname=request.POST['surname'],
            email=request.POST['email'],
            special_requirements=request.POST.get('special_requirements', ''),
            guest_count=request.POST['guest_count'],
            booking_date=request.POST['booking_date'],
            booking_time=request.POST['booking_time'],
        )
        return redirect('index')  # Or another page
    return render(request, 'reservation/reservation.html')  # This matches your template

