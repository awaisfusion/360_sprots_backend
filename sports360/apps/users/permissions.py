from rest_framework.permissions import BasePermission, IsAuthenticated


class IsCustomer(IsAuthenticated):
    """Only customers can access"""
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_customer()


class IsBusiness(IsAuthenticated):
    """Only business users can access"""
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_business()


class IsAdmin(IsAuthenticated):
    """Only admin users can access"""
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_admin()


class IsBusinessOwner(IsAuthenticated):
    """Only the business owner can modify their locations/facilities"""
    def has_object_permission(self, request, view, obj):
        return obj.business == request.user


class IsCustomerOrReadOnly(IsAuthenticated):
    """Customers can read, businesses and admins can read/write their data"""
    def has_permission(self, request, view):
        if request.method in ['GET']:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET']:
            return True
        if hasattr(obj, 'business'):
            return obj.business == request.user
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return False
