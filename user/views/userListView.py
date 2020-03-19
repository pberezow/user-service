from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from user.models import User
from user.serializers import UserDetailsSerializer, UserSimpleSerializer
from user_service.permissions import CustomIsAuthenticated as IsAuthenticated


class UsersListView(ListAPIView):  # GET
    """
    List all users with same licence id
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.is_admin:
            return UserDetailsSerializer
        else:
            return UserSimpleSerializer

    def get_queryset(self):
        qs = User.objects.filter(licence_id=self.request.user.licence_id)
        return qs

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        if not request.user.is_admin:
            qs = qs.filter(is_active=True)

        serializer = self.get_serializer_class()
        users_list = serializer(qs, many=True, context={'request': request})

        return Response(users_list.data)
