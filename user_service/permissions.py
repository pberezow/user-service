from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin


class IsSpecifiedUser(BasePermission):
    def has_permission(self, request, view):
        return view.kwargs['user_id'] == request.user.id
