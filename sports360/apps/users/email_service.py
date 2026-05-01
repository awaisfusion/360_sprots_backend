from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from apps.users.models import EmailVerification


def send_verification_email(user):
    """Send verification code to user's email"""
    # Generate verification code
    code = EmailVerification.generate_code()

    # Create or update verification record
    verification, created = EmailVerification.objects.get_or_create(
        user=user,
        defaults={
            'code': code,
            'expires_at': timezone.now() + timedelta(minutes=10)
        }
    )

    # Update code if exists
    if not created:
        verification.code = code
        verification.expires_at = timezone.now() + timedelta(minutes=10)
        verification.is_verified = False
        verification.attempts = 0
        verification.save()

    # Send email
    subject = '🏟️ Your Email Verification Code for 360 Sports Platform'
    message = f"""
    Hello {user.first_name or user.username},

    Welcome to 360 Sports Platform! 🎉

    Your email verification code is: {code}

    This code will expire in 10 minutes. If you didn't request this code, please ignore this email.

    ✅ Step-by-step:
    1. Copy the code: {code}
    2. Enter it in the app
    3. Complete your registration

    Best regards,
    360 Sports Platform Team
    """

    html_message = f"""
    <html>
        <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
            <div style="max-width: 600px; background-color: white; margin: 0 auto; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h2 style="color: #333;">Email Verification - 360 Sports Platform</h2>
                <p>Hello <strong>{user.first_name or user.username}</strong>,</p>
                <p>Welcome to 360 Sports Platform! 🎉</p>

                <p style="margin-top: 30px;">Your email verification code is:</p>
                <div style="background-color: #f0f0f0; padding: 20px; text-align: center; border-radius: 5px; margin: 20px 0;">
                    <h1 style="color: #2196F3; margin: 0; letter-spacing: 5px;">{code}</h1>
                </div>

                <p style="color: #666; font-size: 14px;">⏰ This code will expire in <strong>10 minutes</strong></p>

                <p style="color: #999; font-size: 12px; margin-top: 30px;">
                    If you didn't request this code, please ignore this email.
                </p>

                <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                <p style="color: #999; font-size: 12px; text-align: center;">
                    © 2026 360 Sports Platform. All rights reserved.
                </p>
            </div>
        </body>
    </html>
    """

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True, "Verification code sent to email"
    except Exception as e:
        return False, f"Error sending email: {str(e)}"


def verify_email_code(user, code):
    """Verify the email code provided by user"""
    try:
        verification = EmailVerification.objects.get(user=user)
    except EmailVerification.DoesNotExist:
        return False, "No verification request found"

    # Check if code is valid
    if not verification.is_valid():
        if verification.is_expired():
            return False, "Verification code has expired"
        if verification.is_verified:
            return False, "Email already verified"
        if verification.attempts >= 5:
            return False, "Too many attempts. Request a new code"

    # Check if code matches
    if verification.code != code:
        verification.attempts += 1
        verification.save()
        remaining = 5 - verification.attempts
        return False, f"Invalid code. {remaining} attempts remaining"

    # Mark as verified
    verification.is_verified = True
    verification.save()

    user.is_verified = True
    user.email_verified_at = timezone.now()
    user.save()

    return True, "Email verified successfully"
