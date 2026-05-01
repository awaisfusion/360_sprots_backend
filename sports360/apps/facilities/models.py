from django.db import models
from apps.locations.models import Location

class Facility(models.Model):
    SPORT_CHOICES = (
        ('badminton', 'Badminton'),
        ('tennis', 'Tennis'),
        ('basketball', 'Basketball'),
        ('football', 'Football'),
        ('swimming', 'Swimming'),
        ('volleyball', 'Volleyball'),
    )

    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='facilities')
    name = models.CharField(max_length=255)
    sport_type = models.CharField(max_length=50, choices=SPORT_CHOICES)
    capacity = models.IntegerField()
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    availability_start = models.TimeField()
    availability_end = models.TimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.sport_type}"
