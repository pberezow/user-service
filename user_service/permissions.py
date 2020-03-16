from rest_framework.permissions import BasePermission, IsAuthenticated


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True
        return request.user.is_admin


class IsSpecifiedUser(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True
        return view.kwargs['user_id'] == request.user.id


class CustomIsAuthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        permitted = super().has_permission(request, view)
        if request.method == 'OPTIONS':
            return True
        return permitted
