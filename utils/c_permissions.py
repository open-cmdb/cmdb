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


class TableLevelPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff or request.method == "OPTIONS":
            return True
        perms = request.user.get_all_permission_names()
        permission_name = view.__class__.__name__
        if request.method in SAFE_METHODS:
            if "read_all" in perms:
                return True
            permission_name = permission_name + ".read"
        else:
            permission_name = permission_name + ".write"
            if "write_all" in perms:
                return True
        return permission_name in perms
