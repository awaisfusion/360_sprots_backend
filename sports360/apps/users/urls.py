from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from apps.users.views import (
    RegisterView, AdminRegisterView, LoginView, UserProfileView,
    SendVerificationCodeView, VerifyEmailView
)

urlpatterns = [
    # Authentication
    path('register/', RegisterView.as_view({'post': 'create'}), name='register'),
    path('register/admin/', AdminRegisterView.as_view({'post': 'create'}), name='admin-register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # Email Verification
    path('send-verification-code/', SendVerificationCodeView.as_view({'post': 'create'}), name='send-verification-code'),
    path('verify-email/', VerifyEmailView.as_view({'post': 'create'}), name='verify-email'),

    # Profile
    path('profile/', UserProfileView.as_view({'get': 'retrieve', 'put': 'update'}), name='user-profile'),
]
