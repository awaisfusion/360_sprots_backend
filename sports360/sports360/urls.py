from django.urls import path, include

urlpatterns = [
    path('api/v1/health/', include('apps.health.urls')),
    path('api/v1/auth/', include('apps.users.urls')),
    path('api/v1/locations/', include('apps.locations.urls')),
    path('api/v1/facilities/', include('apps.facilities.urls')),
    path('api/v1/bookings/', include('apps.bookings.urls')),
    path('api/v1/payments/', include('apps.payments.urls')),
    path('api/v1/notifications/', include('apps.notifications.urls')),
]
