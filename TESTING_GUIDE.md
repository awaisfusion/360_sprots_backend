# Quick Start - Testing Guide

## 🚀 Running the Server

```bash
# Navigate to project
cd /Users/fusionwave/360/sports360

# Activate virtual environment
source ../venv/bin/activate

# Run server
python manage.py runserver 0.0.0.0:8000
```

Server will be available at: **http://localhost:8000**

---

## 📋 Testing with Postman

### Import Collection

1. Open **Postman**
2. Click `File` → `Import`
3. Select `/Users/fusionwave/360/Postman_Collection.json`
4. Click `Import`

### Set Up Environment Variables

The collection has these variables:
- `access_token` - Customer JWT token (auto-filled after login)
- `refresh_token` - Customer refresh token
- `business_access_token` - Business JWT token
- `business_refresh_token` - Business refresh token

---

## 🧪 Testing Workflow

### Step 1: Test Health Endpoint
```
GET /api/v1/health/
```
Expected: 200 OK with "healthy" status

### Step 2: Register Customer
```
POST /api/v1/auth/register/
```
Use the "Register - Customer" request from Postman collection
- Creates customer account
- No auth required

### Step 3: Register Business
```
POST /api/v1/auth/register/
```
Use the "Register - Business" request from Postman collection
- Creates business account
- Requires business details

### Step 4: Login (Customer)
```
POST /api/v1/auth/login/
```
- Username: `john_customer`
- Password: `SecurePass123`
- **Postman automatically stores** `access_token` and `refresh_token`

### Step 5: Get Profile
```
GET /api/v1/auth/profile/
```
Authorization: `Bearer <access_token>`
- Uses the token from Step 4
- Should return your customer profile

### Step 6: Update Profile
```
PUT /api/v1/auth/profile/
```
Authorization: `Bearer <access_token>`
- Update your first_name, last_name, phone
- Verify changes with GET profile

### Step 7: Login (Business)
```
POST /api/v1/auth/login/
```
- Username: `sports_arena`
- Password: `SecurePass123`
- **Postman automatically stores** `business_access_token`

---

## 🔄 Token Management

### Access Token Expired?

Use the **Refresh Token** request:
```
POST /api/v1/auth/token/refresh/
```
Body: `{"refresh": "{{refresh_token}}"}`

Postman will auto-update the `access_token`

---

## 📝 Example Payloads

### Customer Registration
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

### Business Registration
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
  "business_description": "Premium multi-sport facility",
  "business_registration_number": "REG123456"
}
```

### Login
```json
{
  "username": "john_customer",
  "password": "SecurePass123"
}
```

### Update Profile
```json
{
  "first_name": "John Updated",
  "phone": "+91-9999999999"
}
```

---

## 🎯 What to Test

### Authentication
- ✅ Register customer
- ✅ Register business (with validation)
- ✅ Login & get tokens
- ✅ Use token to access profile
- ✅ Refresh token
- ✅ Update profile

### Authorization
- ✅ Access token gives 200 OK
- ✅ No token gives 401 Unauthorized
- ✅ Invalid token gives 401 Unauthorized
- ✅ Expired token requires refresh

### Validation
- ✅ Passwords must match
- ✅ Password minimum 8 chars
- ✅ Email must be unique
- ✅ Username must be unique
- ✅ Business must have business_name & business_registration_number

---

## 🐛 Troubleshooting

### Server Not Starting?
```bash
# Check if port 8000 is already in use
lsof -i :8000

# If in use, kill the process
kill -9 <PID>

# Try again
python manage.py runserver 0.0.0.0:8000
```

### Token Not Working?
- Make sure token is copied correctly
- Check token format: `Authorization: Bearer <token>`
- Not just: `Authorization: <token>`

### Database Errors?
```bash
# Recreate database
rm db.sqlite3
python manage.py migrate
```

### Import Issues?
- Make sure you're using the Postman collection from this repo
- Import directly into Postman (don't copy-paste)

---

## 📚 Additional Resources

- **API Endpoints**: See `API_ENDPOINTS.md`
- **Project Status**: See `PROJECT_STATUS.md`
- **Postman Collection**: `Postman_Collection.json`

---

## 🎓 Learning Path

1. **Start**: Health endpoint (no auth needed)
2. **Then**: Register and Login
3. **Next**: Get/Update Profile
4. **Later**: Locations, Facilities, Bookings (when ready)

---

**Ready to test!** 🚀

Any issues? Check the error response for details.
