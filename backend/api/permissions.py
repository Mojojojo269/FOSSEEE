from rest_framework import permissions


class IsAuthenticatedCustom(permissions.BasePermission):
    """
    Custom permission to require authentication for all endpoints except login.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
