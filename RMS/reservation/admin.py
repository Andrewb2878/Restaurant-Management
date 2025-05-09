from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'surname', 'email', 'booking_date', 'booking_time', 'guest_count')
    search_fields = ('first_name', 'surname', 'email')
    list_filter = ('booking_date', 'booking_time')

