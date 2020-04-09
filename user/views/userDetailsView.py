from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_302_FOUND, \
    HTTP_204_NO_CONTENT, HTTP_201_CREATED, HTTP_200_OK

from user.models import User
from user.serializers import UserDetailsSerializer
from user_service.permissions import IsAdminUser, IsSpecifiedUser, CustomIsAuthenticated as IsAuthenticated
from user_service.exceptions import UserDoesNotExist, OnlyForAdmin


class UserDetailsView(RetrieveUpdateDestroyAPIView):  # GET, PUT, DELETE
    """
    Retrieve, update or delete specified user
    """
    permission_classes = [IsAuthenticated & (IsAdminUser | IsSpecifiedUser)]
    serializer_class = UserDetailsSerializer

    def get_queryset(self):
        qs = User.objects.filter(licence_id=self.request.user.licence_id)
        return qs

    def retrieve(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']

        user = self.get_queryset().filter(pk=user_id)
        if not user.exists():
            raise UserDoesNotExist()
        user = user.get()

        serializer = self.get_serializer_class()
        user_to = serializer(user)

        return Response(user_to.data)

    def update(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']

        if not request.user.is_admin and request.user.pk != user_id:
            raise OnlyForAdmin()

        user = self.get_queryset().filter(pk=user_id)
        if not user.exists():
            raise UserDoesNotExist()
        user = user.get()

        serializer = self.get_serializer_class()

        user_to = serializer(user, data=request.data)
        user_to.is_valid(raise_exception=True)

        user_to.save(updating_user=request.user)

        return Response(user_to.data)

    def destroy(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']

        if not request.user.is_admin:
            raise OnlyForAdmin()

        user = self.get_queryset().filter(pk=user_id)
        if not user.exists():
            raise UserDoesNotExist()
        user = user.get()

        user.is_active = False
        user.save()

        return Response(status=HTTP_204_NO_CONTENT)
