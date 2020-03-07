from django.db.utils import IntegrityError
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_302_FOUND, \
    HTTP_204_NO_CONTENT, HTTP_201_CREATED

from group.models import Group
from user.models import User
from user.serializers import UserDetailsSerializer, UserSimpleSerializer, CreateUserSerializer, UserSetGroupSerializer, \
    UserSetPasswordSerializer
from user_service.permissions import IsAdminUser, IsSpecifiedUser

# TODO - Add custom error messages


class RegisterView(CreateAPIView):  # POST
    """
    Create new user
    """
    permission_classes = [IsAuthenticated & IsAdminUser]
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        # if not request.user.is_admin:
        #     return Response({'error': 'Only admin can create new users!'}, status=HTTP_403_FORBIDDEN)

        form_data = request.data
        form_data['licence_id'] = request.user.licence_id

        serializer = self.get_serializer_class()
        user = serializer(data=form_data)

        user.is_valid(raise_exception=True)
        try:
            user_instance = user.save()
        except IntegrityError as e:
            return Response({'details': e.__repr__()}, status=HTTP_400_BAD_REQUEST)

        user_to = UserDetailsSerializer(user_instance)

        return Response(user_to.data, status=HTTP_201_CREATED)


class LogoutView(RetrieveAPIView):  # GET
    """
    Logout - remove token cookie
    """
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        resp = Response()
        resp.delete_cookie('token')
        return resp


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

        # if not request.user.is_admin and request.user.pk != user_id:
        #     return Response(status=HTTP_403_FORBIDDEN)

        user = self.get_queryset().filter(pk=user_id)
        if not user.exists():
            return Response(status=HTTP_404_NOT_FOUND)
        user = user.get()

        serializer = self.get_serializer_class()
        user_to = serializer(user)

        return Response(user_to.data, status=HTTP_302_FOUND)

    def update(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']

        if not request.user.is_admin and request.user.pk != user_id:
            return Response(status=HTTP_403_FORBIDDEN)

        user = self.get_queryset().filter(pk=user_id)
        if not user.exists():
            return Response(status=HTTP_404_NOT_FOUND)
        user = user.get()

        serializer = self.get_serializer_class()

        user_to = serializer(user, data=request.data)
        user_to.is_valid(raise_exception=True)

        user_to.save(updating_user=request.user)

        return Response(user_to.data)

    def destroy(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']

        if not request.user.is_admin:
            return Response(status=HTTP_403_FORBIDDEN)

        user = self.get_queryset().filter(pk=user_id)
        if not user.exists():
            return Response(status=HTTP_404_NOT_FOUND)
        user = user.get()

        user.is_active = False
        user.save()

        return Response(status=HTTP_204_NO_CONTENT)


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
            return Response(status=HTTP_404_NOT_FOUND)
        user = user.get()

        serializer = self.get_serializer_class()
        user_to = serializer(user, request.data)
        user_to.is_valid(raise_exception=True)
        user_to.save(updating_user=request.user)

        return Response(user_to.data)


class SetAvatarView(UpdateAPIView):  # PUT
    # TODO
    pass


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
            return Response(status=HTTP_404_NOT_FOUND)
        user = user.get()

        serializer = self.get_serializer_class()
        groups = request.data.get('groups', None)
        if groups is None:
            return Response(status=HTTP_400_BAD_REQUEST)

        try:
            groups_instances = Group.objects.filter(licence_id=user.licence_id, name__in=[g['name'] for g in groups])
        except KeyError as e:
            return Response(status=HTTP_400_BAD_REQUEST)

        if len([g['name'] for g in groups]) != groups_instances.count():
            return Response(status=HTTP_400_BAD_REQUEST)

        user.groups.clear()
        for group in groups_instances:
            user.groups.add(group)
        user.save()

        user_to = serializer(user)

        return Response(user_to.data)


class FooView(ListAPIView):
    def list(self, request, *args, **kwargs):
        return Response({'status': 'UP'})
