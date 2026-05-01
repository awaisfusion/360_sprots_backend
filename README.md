# 360 Sports Platform - Backend API

## Role Structure

The platform has **three distinct user roles** with different capabilities:

### 1. **Customer** 
- Browse and search locations & facilities
- Make bookings for sports facilities
- View booking history
- Manage favorite locations
- Make repeat bookings
- Receive booking confirmations & notifications
- Pay for bookings

### 2. **Business** (Facility Operators)
- Create and manage locations (sports facilities)
- Add multiple facilities per location
- Set pricing and availability schedules
- Manage time slots and capacity
- View live and historical bookings
- Track revenue and utilization reports
- Manage booking requests and cancellations
- Export reports (daily, weekly, monthly)

### 3. **Admin** (Platform Administrators)
- Full system access
- Manage all users (customers & businesses)
- Handle support tickets and disputes
- View platform-wide analytics
- Manage payments and transactions
- System configuration and monitoring

## Architecture Overview

Clean Django REST Framework API with modular app structure:

```
sports360/
├── sports360/          # Project config (settings, urls, wsgi, asgi)
├── apps/
│   ├── health/         # Health check endpoint
│   ├── users/          # Authentication & user management
│   ├── locations/      # Sports facility locations
│   ├── facilities/     # Individual sports facilities
│   ├── bookings/       # Booking management
│   ├── payments/       # Payment processing
│   └── notifications/  # Email & push notifications
```

## Setup Instructions

### 1. Install Dependencies
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
cd sports360
python manage.py migrate
```

### 3. Start Development Server
```bash
python manage.py runserver 0.0.0.0:8000
```

### 4. Test Health Endpoint
```bash
curl http://localhost:8000/api/v1/health/
```

## API Endpoints

### Health Check
- **GET** `/api/v1/health/` - Server status

## Authentication Examples

### Customer Registration
```json
POST /api/v1/auth/register/
{
  "email": "customer@example.com",
  "username": "john_customer",
  "password": "securepass123",
  "password2": "securepass123",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+91-9876543210",
  "role": "customer"
}
```

### Business Registration
```json
POST /api/v1/auth/register/
{
  "email": "business@example.com",
  "username": "sports_arena",
  "password": "securepass123",
  "password2": "securepass123",
  "first_name": "Sports",
  "last_name": "Arena",
  "phone": "+91-9876543210",
  "role": "business",
  "business_name": "Sports Arena Mumbai",
  "business_description": "Premium multi-sport facility",
  "business_registration_number": "REG123456"
}
```

### Login
```json
POST /api/v1/auth/login/
{
  "username": "john_customer",
  "password": "securepass123"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Locations (Coming Next)
- GET `/api/v1/locations/` - List all locations
- POST `/api/v1/locations/` - Create location (admin only)
- GET `/api/v1/locations/{id}/` - Location details

### Facilities (Coming Next)
- GET `/api/v1/facilities/` - List all facilities
- POST `/api/v1/facilities/` - Create facility (admin only)

### Bookings (Coming Next)
- GET `/api/v1/bookings/` - User bookings
- POST `/api/v1/bookings/` - Create booking
- PUT `/api/v1/bookings/{id}/` - Update booking

### Payments (Coming Next)
- POST `/api/v1/payments/` - Process payment

### Notifications (Coming Next)
- GET `/api/v1/notifications/` - User notifications

## Database Models

**User** (Custom AbstractUser)
- Three roles: customer, business, admin
- Email verification support
- Phone number field
- Business-specific fields (business_name, registration_number)
- Role helper methods: is_customer(), is_business(), is_admin()

**Location**
- Managed by Business users only
- Operating hours configuration
- Geographic coordinates for mapping
- Multiple facilities per location

**Facility**
- Sport type (badminton, tennis, basketball, football, swimming, volleyball)
- Pricing per hour
- Availability schedule
- Capacity management

**Booking**
- Links Customer + Facility
- Date/time slot management
- Status tracking (pending, confirmed, cancelled)
- Real-time availability locking

**Payment**
- Multiple payment methods (card, Apple Pay, Google Pay)
- Transaction tracking
- Status management (pending, completed, failed, refunded)

**Notification**
- User notifications
- Types: booking_confirmed, payment_received, reminder, etc.
- Read/unread tracking

## Environment Variables

```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

JWT_ACCESS_TOKEN_LIFETIME=15
JWT_REFRESH_TOKEN_LIFETIME=7
```

## Key Features (So Far)

✅ Clean, modular app structure  
✅ Health endpoint for server monitoring  
✅ Three-tier role system (customer, business, admin)
✅ User registration & JWT authentication  
✅ Role-based access control with permission classes
✅ User profile management  
✅ Database models for all core features  
✅ CORS enabled for mobile/frontend integration  

## Role-Based Access Control

Permission classes available in `apps/users/permissions.py`:

- **IsCustomer** - Only customers can access
- **IsBusiness** - Only business users can access
- **IsAdmin** - Only admin users can access
- **IsBusinessOwner** - Only business owner can modify their resources
- **IsCustomerOrReadOnly** - Public read access, authenticated write access

## Next Steps

1. Build Locations CRUD endpoints
2. Build Facilities CRUD with filtering
3. Build Bookings with real-time availability locking
4. Add Payment processing integration
5. Add Notification services (email, push)
6. Add Admin dashboard endpoints
7. Add search & filtering
8. Add reporting & analytics

---

**Technology Stack**
- Django 6.0.4
- Django REST Framework 3.14.0
- SimpleJWT 5.5.1
- CORS Headers 4.3.0
- SQLite (development) / PostgreSQL (production)
# 360_sprots_backend
