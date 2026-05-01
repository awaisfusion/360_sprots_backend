from django.db import models
from django.core.exceptions import ValidationError
from apps.users.models import User

class Location(models.Model):
    business = models.ForeignKey(User, on_delete=models.CASCADE, related_name='locations',
                                 limit_choices_to={'role': 'business'}, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    operating_hours_start = models.TimeField()
    operating_hours_end = models.TimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    def __str__(self):
        return f"{self.name} ({self.business.business_name if self.business else 'Unassigned'})"

    def save(self, *args, **kwargs):
        if self.business and self.business.role != 'business':
            raise ValidationError('Location can only be assigned to business users')
        super().save(*args, **kwargs)
