# Email Verification & Admin Registration - Complete Guide

## 🎯 New Features Added

### 1. Email Verification System
- Send 6-digit verification code to user's email
- Verify email with code before full account activation
- Resend code if needed
- 10-minute code expiration
- 5-attempt limit before lockout

### 2. Admin Registration
- Only existing admins can create new admins
- Admins are automatically verified (no email verification needed)
- Full admin access upon creation

---

## 📧 Email Verification Flow

### Step 1: Register User (Customer or Business)

**Endpoint:**
```
POST /api/v1/auth/register/
```

**Request:**
```json
{
  "email": "customer@example.com",
  "username": "john_customer",
  "password": "SecurePass123",
  "password2": "SecurePass123",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+91-9876543210",
  "role": "customer"
}
```

**Response (201 Created):**
```json
{
  "message": "User registered successfully. Verification code sent to email.",
  "user": {
    "id": 1,
    "email": "customer@example.com",
    "username": "john_customer",
    "first_name": "John",
    "role": "customer",
    "is_verified": false,
    "email_verified_at": null
  },
  "email_sent": true,
  "next_step": "Verify your email with the code sent to customer@example.com"
}
```

**What happens:**
- ✅ User account created with `is_verified=false`
- ✅ Verification code sent to email (6 digits)
- ✅ Code expires in 10 minutes
- ✅ User cannot login until email is verified (future enforcement)

---

### Step 2: Send Verification Code (Resend)

If user didn't receive the code, they can request a new one.

**Endpoint:**
```
POST /api/v1/auth/send-verification-code/
```

**Request:**
```json
{
  "email": "customer@example.com"
}
```

**Response (200 OK):**
```json
{
  "message": "Verification code sent to email",
  "email": "customer@example.com",
  "code_sent": true
}
```

**Notes:**
- Can be called multiple times
- Generates new code each time
- Previous code is invalidated
- Rate limiting coming soon (to prevent abuse)

---

### Step 3: Verify Email with Code

User enters the 6-digit code received in email.

**Endpoint:**
```
POST /api/v1/auth/verify-email/
```

**Request:**
```json
{
  "email": "customer@example.com",
  "code": "123456"
}
```

**Success Response (200 OK):**
```json
{
  "message": "Email verified successfully",
  "user": {
    "id": 1,
    "email": "customer@example.com",
    "username": "john_customer",
    "is_verified": true,
    "email_verified_at": "2026-05-01T12:30:45.123456Z"
  },
  "verified": true
}
```

**Error Responses:**

Invalid code:
```json
{
  "message": "Invalid code. 4 attempts remaining"
}
```

Code expired:
```json
{
  "message": "Verification code has expired"
}
```

Too many attempts:
```json
{
  "message": "Too many attempts. Request a new code"
}
```

---

## 👨‍💼 Admin Registration

### Create Admin Account (Admin Only)

Only existing admins can create new admin accounts.

**Endpoint:**
```
POST /api/v1/auth/register/admin/
Authorization: Bearer <admin_access_token>
```

**Request:**
```json
{
  "email": "newadmin@example.com",
  "username": "new_admin",
  "password": "SecurePass123",
  "password2": "SecurePass123",
  "first_name": "New",
  "last_name": "Admin",
  "phone": "+91-9876543212"
}
```

**Response (201 Created):**
```json
{
  "message": "Admin created successfully",
  "user": {
    "id": 3,
    "email": "newadmin@example.com",
    "username": "new_admin",
    "first_name": "New",
    "last_name": "Admin",
    "role": "admin",
    "role_display": "Admin",
    "phone": "+91-9876543212",
    "is_verified": true,
    "email_verified_at": "2026-05-01T12:30:45.123456Z"
  }
}
```

**Error Response (403 Forbidden):**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

**Notes:**
- ✅ Admin is automatically verified (no email verification needed)
- ✅ Admin can login immediately
- ✅ Only admins can create admins
- ✅ Non-admin users get 403 Forbidden

---

## 🧪 Complete Testing Workflow

### Using Postman:

**1. Register Customer:**
- Use: "1️⃣ Register - Customer"
- Copy email from response

**2. Send Verification Code:**
- Use: "2️⃣ Send Verification Code"
- Check console output for verification code (console backend)
- Copy the 6-digit code

**3. Verify Email:**
- Use: "3️⃣ Verify Email (With Code from Email)"
- Paste the 6-digit code
- Should return verified=true

**4. Login:**
- Use: "Login - Customer"
- This automatically stores access_token

**5. Get Profile:**
- Use: "Get User Profile"
- Should show is_verified=true

---

## 📧 Email Configuration

### Development (Console Backend)

**Default in `.env`:**
```
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

**Output:** Verification codes printed to server console

```
Subject: 🏟️ Your Email Verification Code for 360 Sports Platform
From: noreply@sports360.com
To: customer@example.com

Body:
Hello John,

Welcome to 360 Sports Platform! 🎉

Your email verification code is: 123456

This code will expire in 10 minutes...
```

### Production (Gmail SMTP)

**Configure in `.env`:**
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@sports360.com
```

**Steps:**
1. Enable 2-factor authentication on Gmail
2. Generate app-specific password
3. Use app password in EMAIL_HOST_PASSWORD
4. Save and test

---

## 🔒 Security Features

- ✅ 6-digit random codes (not sequential)
- ✅ 10-minute expiration
- ✅ 5-attempt limit before lockout
- ✅ Hashed storage (future enhancement)
- ✅ Rate limiting (coming soon)
- ✅ Admin creation restricted to admins only
- ✅ Automatic admin verification

---

## 📊 Database Models

### EmailVerification Model

```python
{
  "id": 1,
  "user": 1,
  "code": "123456",
  "created_at": "2026-05-01T12:20:45Z",
  "expires_at": "2026-05-01T12:30:45Z",
  "is_verified": false,
  "attempts": 0
}
```

### User Model (Updated)

```python
{
  "id": 1,
  "email": "customer@example.com",
  "is_verified": false,
  "email_verified_at": null,
  "role": "customer"
}
```

---

## ❌ Error Handling

| Error | Status | Cause |
|-------|--------|-------|
| Passwords do not match | 400 | password != password2 |
| Email already verified | 400 | User.is_verified=true |
| Code expired | 400 | timezone.now() > expires_at |
| Invalid code | 400 | code doesn't match |
| Too many attempts | 400 | attempts >= 5 |
| User not found | 404 | Email doesn't exist |
| No permission | 403 | Not an admin (for admin registration) |

---

## 🎯 Next Steps

- ✅ Email verification system complete
- ✅ Admin registration complete
- 📋 Password reset endpoint
- 📋 Email change verification
- 📋 SMS verification (optional)
- 📋 Two-factor authentication
- 📋 OAuth2 integration

---

## 📝 Notes

- Verification code sent to console by default
- Change EMAIL_BACKEND to smtp.EmailBackend for production
- Check `.env` for email configuration
- Update Postman collection version to v2
- All endpoints return JSON responses
- Errors include helpful messages

---

**Last Updated:** May 1, 2026
**Status:** Email Verification & Admin Registration Ready ✅
