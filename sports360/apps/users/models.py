from django.db import models
from django.contrib.auth.models import AbstractUser
import secrets
import string

class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('business', 'Business'),
        ('admin', 'Admin'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=15, blank=True)
    is_verified = models.BooleanField(default=False)
    email_verified_at = models.DateTimeField(null=True, blank=True)

    # Business-specific fields
    business_name = models.CharField(max_length=255, blank=True, null=True)
    business_description = models.TextField(blank=True, null=True)
    business_registration_number = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

    def is_customer(self):
        return self.role == 'customer'

    def is_business(self):
        return self.role == 'business'

    def is_admin(self):
        return self.role == 'admin'


class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='verification')
    code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Email Verification'
        verbose_name_plural = 'Email Verifications'

    def __str__(self):
        return f"Verification for {self.user.email}"

    @staticmethod
    def generate_code():
        """Generate a random 6-digit code"""
        return ''.join(secrets.choice(string.digits) for _ in range(6))

    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.expires_at

    def is_valid(self):
        return not self.is_expired() and not self.is_verified and self.attempts < 5
