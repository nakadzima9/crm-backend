from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsUser(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return bool(request.user and request.user.is_authenticated)


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.user_type == 'admin')


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and
                    request.user.user_type == 'manager' and request.method in SAFE_METHODS)


