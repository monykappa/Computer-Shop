
from rest_framework.permissions import BasePermission # type: ignore

class IsSuperAdmin(BasePermission):
    """
    Custom permission to only allow superadmins to access the API.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
