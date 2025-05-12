from django.db import models

# Create your models here.
class InventoryItem(models.Model):
    """Model for inventory items."""

    name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    unit = models.CharField(max_length=20)
    min_level = models.DecimalField(max_digits=8, decimal_places=2)
    supplier = models.CharField(max_length=100)
    last_ordered = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"

    def is_low(self):
        """Check if the inventory level is below the minimum threshold."""
        return self.quantity <= self.min_level
