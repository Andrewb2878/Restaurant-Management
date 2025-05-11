from django.contrib import admin
from .models import Reservation, Table

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'surname', 'email', 'booking_date', 'booking_time', 'guest_count')
    search_fields = ('first_name', 'surname', 'email')
    list_filter = ('booking_date', 'booking_time')


class TableAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'status')
    readonly_fields = ('booking_record',)
    search_fields = ('table_number',)
    list_filter = ('status',)