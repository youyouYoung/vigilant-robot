from rest_framework.permissions import BasePermission

class AdminOnly(BasePermission):
    """
    Custom permission to allow only admins to modify objects.
    Other users can only read.
    """
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'
