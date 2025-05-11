from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db import models

class Reservation(models.Model):
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    special_requirements = models.TextField(blank=True, null=True)
    guest_count = models.PositiveIntegerField()
    booking_date = models.DateField()
    booking_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.surname} - {self.booking_date} {self.booking_time}"


class Table(models.Model):
    TABLE_STATUS_CHOICES = [
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('occupied', 'Occupied'),
    ]
    table_number = models.PositiveIntegerField(unique=True)
    status = models.CharField(max_length=10, choices=TABLE_STATUS_CHOICES, default='available')
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True, blank=True)
    booking_record = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Table {self.table_number} ({self.status})"

@receiver(post_delete, sender=Reservation)
def update_table_status_on_reservation_delete(sender, instance, **kwargs):
    # Check if the reservation has a linked table
    if instance.table:
        # Set the table status to "Available"
        instance.table.status = 'available'
        instance.table.save()