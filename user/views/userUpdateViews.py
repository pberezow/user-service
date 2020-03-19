from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_302_FOUND, \
    HTTP_204_NO_CONTENT, HTTP_201_CREATED

from group.models import Group
from user.models import User
from user.serializers import UserSetGroupSerializer, UserSetPasswordSerializer
from user_service.permissions import IsAdminUser, IsSpecifiedUser, CustomIsAuthenticated as IsAuthenticated
from user_service.exceptions import UserDoesNotExist, InvalidRequestData, InvalidGroupName


class SetUsersPasswordView(UpdateAPIView):
    """
    Set password
    """
    permission_classes = [IsAuthenticated & (IsAdminUser | IsSpecifiedUser)]
    serializer_class = UserSetPasswordSerializer

    def get_queryset(self):
        return User.objects.filter(licence_id=self.request.user.licence_id)

    def update(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']

        user = self.get_queryset().filter(pk=user_id)
        if not user.exists():
            raise UserDoesNotExist()
        user = user.get()

        serializer = self.get_serializer_class()
        user_to = serializer(user, request.data)
        user_to.is_valid(raise_exception=True)
        user_to.save(updating_user=request.user)

        return Response(user_to.data)


class SetAvatarView(UpdateAPIView):  # PUT
    # TODO
    def update(self, request, *args, **kwargs):
        return Response({'details': 'Not implemented yet.'})


class SetUserGroupsView(UpdateAPIView):  # PUT
    """
    Set user's permission groups
    """
    permission_classes = [IsAuthenticated & IsAdminUser]
    serializer_class = UserSetGroupSerializer

    def get_queryset(self):
        licence_id = self.request.user.licence_id
        qs = User.objects.filter(licence_id=licence_id)
        return qs

    def update(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']

        user = self.get_queryset().filter(pk=user_id)
        if not user.exists():
            raise UserDoesNotExist()
        user = user.get()

        serializer = self.get_serializer_class()
        groups = request.data.get('groups', None)
        if groups is None:
            raise InvalidRequestData()

        try:
            groups_instances = Group.objects.filter(licence_id=user.licence_id, name__in=[g['name'] for g in groups])
        except KeyError as e:
            raise InvalidRequestData()

        if len([g['name'] for g in groups]) != groups_instances.count():
            raise InvalidGroupName()

        user.groups.clear()
        for group in groups_instances:
            user.groups.add(group)
        user.save()

        user_to = serializer(user)

        return Response(user_to.data)
