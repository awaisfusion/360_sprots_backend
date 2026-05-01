# 360 Sports Platform - API Endpoints Documentation

**Base URL**: `http://localhost:8000/api/v1`

---

## 🏥 Health & Status

### Health Check
Check if the API server is running.

```
GET /health/
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "message": "Sports360 API is running",
  "django_version": "6.0.4"
}
```

**No authentication required** ✅

---

## 🔐 Authentication Endpoints

### 1. Register - Customer

Create a new customer account.

```
POST /auth/register/
Content-Type: application/json
```

**Request Body:**
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
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "customer@example.com",
    "username": "john_customer",
    "first_name": "John",
    "last_name": "Doe",
    "role": "customer",
    "role_display": "Customer",
    "phone": "+91-9876543210",
    "is_verified": false,
    "business_name": null,
    "business_description": null
  }
}
```

**Notes:**
- Password must be at least 8 characters
- Both passwords must match
- Email must be unique
- Username must be unique
- Phone is optional

---

### 2. Register - Business

Create a new business account for facility operators.

```
POST /auth/register/
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "business@example.com",
  "username": "sports_arena",
  "password": "SecurePass123",
  "password2": "SecurePass123",
  "first_name": "Sports",
  "last_name": "Arena",
  "phone": "+91-9876543211",
  "role": "business",
  "business_name": "Sports Arena Mumbai",
  "business_description": "Premium multi-sport facility in Mumbai",
  "business_registration_number": "REG123456"
}
```

**Response (201 Created):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 2,
    "email": "business@example.com",
    "username": "sports_arena",
    "first_name": "Sports",
    "last_name": "Arena",
    "role": "business",
    "role_display": "Business",
    "phone": "+91-9876543211",
    "is_verified": false,
    "business_name": "Sports Arena Mumbai",
    "business_description": "Premium multi-sport facility in Mumbai"
  }
}
```

**Notes:**
- For business role, `business_name` and `business_registration_number` are **required**
- `business_description` is optional

---

### 3. Login

Authenticate and get JWT tokens.

```
POST /auth/login/
Content-Type: application/json
```

**Request Body:**
```json
{
  "username": "john_customer",
  "password": "SecurePass123"
}
```

**Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**JWT Token includes:**
- User ID
- Email
- Username
- Role (customer, business, admin)
- is_business flag
- is_admin flag

**Notes:**
- `access` token expires in 15 minutes (configurable)
- `refresh` token expires in 7 days (configurable)
- Use `access` token in Authorization header for all protected endpoints
- Include token as: `Authorization: Bearer <access_token>`

---

### 4. Refresh Token

Get a new access token using refresh token.

```
POST /auth/token/refresh/
Content-Type: application/json
Authorization: Bearer <any_token>
```

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

### 5. Get User Profile

Retrieve the authenticated user's profile.

```
GET /auth/profile/
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "customer@example.com",
  "username": "john_customer",
  "first_name": "John",
  "last_name": "Doe",
  "role": "customer",
  "role_display": "Customer",
  "phone": "+91-9876543210",
  "is_verified": false,
  "business_name": null,
  "business_description": null
}
```

**Authentication:** Required ✅

---

### 6. Update User Profile

Update the authenticated user's profile.

```
PUT /auth/profile/
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body (all fields optional):**
```json
{
  "first_name": "John Updated",
  "last_name": "Doe Updated",
  "phone": "+91-9999999999"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "customer@example.com",
  "username": "john_customer",
  "first_name": "John Updated",
  "last_name": "Doe Updated",
  "role": "customer",
  "role_display": "Customer",
  "phone": "+91-9999999999",
  "is_verified": false,
  "business_name": null,
  "business_description": null
}
```

**Authentication:** Required ✅

**Notes:**
- Cannot change email, username, or role through this endpoint
- Password changes require separate endpoint (coming soon)

---

## 📍 Locations Endpoints (Coming Soon)

### List Locations
```
GET /locations/
Authorization: Bearer <access_token>
```

### Create Location (Business Only)
```
POST /locations/
Authorization: Bearer <access_token>
Content-Type: application/json
```

### Get Location Detail
```
GET /locations/{id}/
Authorization: Bearer <access_token>
```

### Update Location (Business Owner Only)
```
PUT /locations/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json
```

### Delete Location (Business Owner Only)
```
DELETE /locations/{id}/
Authorization: Bearer <access_token>
```

---

## 🏐 Facilities Endpoints (Coming Soon)

### List Facilities
```
GET /facilities/
Authorization: Bearer <access_token>
```

### Create Facility (Business Only)
```
POST /facilities/
Authorization: Bearer <access_token>
Content-Type: application/json
```

### Get Facility Detail
```
GET /facilities/{id}/
Authorization: Bearer <access_token>
```

### Update Facility (Business Owner Only)
```
PUT /facilities/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json
```

---

## 📅 Bookings Endpoints (Coming Soon)

### List My Bookings
```
GET /bookings/
Authorization: Bearer <access_token>
```

### Create Booking
```
POST /bookings/
Authorization: Bearer <access_token>
Content-Type: application/json
```

### Get Booking Detail
```
GET /bookings/{id}/
Authorization: Bearer <access_token>
```

### Cancel Booking
```
DELETE /bookings/{id}/
Authorization: Bearer <access_token>
```

---

## 💳 Payments Endpoints (Coming Soon)

### Process Payment
```
POST /payments/
Authorization: Bearer <access_token>
Content-Type: application/json
```

### Get Payment Status
```
GET /payments/{id}/
Authorization: Bearer <access_token>
```

---

## 🔔 Notifications Endpoints (Coming Soon)

### Get Notifications
```
GET /notifications/
Authorization: Bearer <access_token>
```

### Mark Notification as Read
```
PUT /notifications/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json
```

---

## Error Responses

### 400 Bad Request
```json
{
  "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Testing Flow

### For Customers:

1. **Register**: `POST /auth/register/` with role="customer"
2. **Login**: `POST /auth/login/` to get tokens
3. **Browse Facilities**: `GET /facilities/`
4. **Create Booking**: `POST /bookings/`
5. **Make Payment**: `POST /payments/`

### For Business Operators:

1. **Register**: `POST /auth/register/` with role="business" + business details
2. **Login**: `POST /auth/login/` to get tokens
3. **Create Location**: `POST /locations/`
4. **Add Facilities**: `POST /facilities/`
5. **View Bookings**: `GET /bookings/`

### For Admins:

Full access to all endpoints (coming soon)

---

## Rate Limiting & Pagination

- Default page size: 20 items
- Pagination: Use `?page=1&page_size=50` in query string
- Rate limiting: Coming soon

---

## Environment Setup

```
BASE_URL=http://localhost:8000/api/v1
```

For Postman:
1. Import `Postman_Collection.json`
2. Create environment with variable `access_token`
3. Run "Login" request first to populate token
4. Other requests will use the stored token

---

**Last Updated**: May 1, 2026
**API Version**: v1
**Status**: Active - Auth endpoints ready, Locations/Facilities coming next
