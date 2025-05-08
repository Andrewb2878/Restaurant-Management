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

