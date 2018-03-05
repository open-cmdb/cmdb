from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

class IsAdminCreate(BasePermission):
    def has_permission(self, request, view):
        return view.action not in ["list", "create"] or request.user.is_staff

class IsAdminOrSelfChange(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and request.user.is_staff
        )