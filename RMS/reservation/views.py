from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import JsonResponse
from .models import Reservation
from .forms import ReservationForm
from datetime import date, datetime, timedelta


def reservation(request):
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            cd = form.cleaned_data
            messages.success(request, f"Thank you {cd['first_name']}, your table has been booked for {cd['booking_date']} at {cd['booking_time']}. You will recive a confirmation email shortly.")
            form.send_confirmation_email()
            
            return redirect('reservation')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = ReservationForm()

    return render(request, 'reservation/reservation.html', {
        'form': form,
        'tomorrow': tomorrow
    })

@login_required
def view_reservations(request):
    current_time = timezone.now()    

    reservations = Reservation.objects.all().order_by('booking_date', 'booking_time')
    for reservation in reservations:
        # Combine the booking_date and booking_time into datetime
        reservation_datetime = datetime.combine(reservation.booking_date, reservation.booking_time)
        reservation_datetime = timezone.make_aware(reservation_datetime, timezone.get_current_timezone())
        reservation.is_past = reservation_datetime < current_time

    return render(request, 'reservation/view_reservations.html', {'reservations': reservations})


@login_required
def delete_reservation(request, id):
    reservation = get_object_or_404(Reservation, id=id)
    reservation.delete()
    return JsonResponse({'success': True})


@login_required
def cancel_reservation(request, id):
    reservation = get_object_or_404(Reservation, id=id)

    send_mail(
        subject='Reservation Cancellation',
        message=(
            f"Dear {reservation.first_name},\n\n"
            f"We regret to inform you that your reservation for {reservation.booking_date} at {reservation.booking_time} "
            f"has been cancelled.\nDetails:\n"
            f"Date: {reservation.booking_date}\nTime: {reservation.booking_time}\nGuests: {reservation.guest_count}\n\n"
            f"Regards,\nMUTLULUK Team"
        ),
        from_email=None,
        recipient_list=[reservation.email],
        fail_silently=False,
    )

    reservation.delete()
    return JsonResponse({'success': True})