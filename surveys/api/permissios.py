from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_superuser

    # def has_object_permission(self, request, view, obj):
    #     return super().has_object_permission(request, view, obj)


class IsAdminOrCreateReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'POST']:
            return True
        return request.user.is_superuser
