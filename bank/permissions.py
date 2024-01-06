# permissions.py
from rest_framework import permissions

class IsLegislator(permissions.BasePermission):
    def has_permission(self, request, view):
        # Implement logic to determine if the user is a legislator
        return request.user.groups.filter(name='Legislators').exists() or request.user.is_legislator
