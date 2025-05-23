from django.db import models
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class MenuItem(models.Model):
    """Model for menu items."""

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=50)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    ingredients = models.TextField(blank=True, null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name



class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField(max_length=1000)
    submitted_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedback"

    def __str__(self):
        return f"{self.name} - {self.subject}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ROLE_CHOICES = (
        ('Waiter', 'Waiter'),
        ('Manager', 'Manager'),
        ('Chef', 'Chef'),
        
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
