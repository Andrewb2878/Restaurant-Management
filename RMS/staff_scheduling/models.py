from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now



class Schedule(models.Model):
    name = models.CharField(max_length=100)  # Example: "Week 1, May 2025"
    start_date = models.DateField()  # Changed from start_time
    end_date = models.DateField()  # Changed from end_time
    staff = models.ManyToManyField(User, related_name="schedules")  # Many-to-many relationship with staff
    date_created = models.DateTimeField(default=now, editable=False)  # Ensures existing rows get a default value
    date_modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.name} ({self.start_date} - {self.end_date})"

class Shift(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="shifts")
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shifts")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    role = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.staff.username} - {self.start_time} to {self.end_time}"