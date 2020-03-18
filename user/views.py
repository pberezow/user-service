from django.db.utils import IntegrityError
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_302_FOUND, \
    HTTP_204_NO_CONTENT, HTTP_201_CREATED
from django.template.loader import render_to_string
from django.core.mail import send_mail

from group.models import Group
from user.models import User, ResetPasswordToken
from user.serializers import UserDetailsSerializer, UserSimpleSerializer, CreateUserSerializer, UserSetGroupSerializer, \
    UserSetPasswordSerializer, ResetPasswordTokenSerializer, ResetPasswordSerializer
from user_service.permissions import IsAdminUser, IsSpecifiedUser, CustomIsAuthenticated as IsAuthenticated
from user_service.exceptions import CustomException, DatabaseError

# TODO - Add custom error messages


class RegisterView(CreateAPIView):  # POST
    """
    Create new user
    """
    permission_classes = [IsAuthenticated & IsAdminUser]
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):

        form_data = request.data or {}
        form_data['licence_id'] = request.user.licence_id

        serializer = self.get_serializer_class()
        user = serializer(data=form_data)

        user.is_valid(raise_exception=True)
        try:
            user_instance = user.save()
        except IntegrityError as e:
            raise CustomException(status_code=HTTP_400_BAD_REQUEST, error_code='E304', error_message=e.__repr__())

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
            raise CustomException(status_code=HTTP_404_NOT_FOUND, error_code='E306')
        user = user.get()

        serializer = self.get_serializer_class()
        user_to = serializer(user)

        return Response(user_to.data, status=HTTP_302_FOUND)

    def update(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']

        if not request.user.is_admin and request.user.pk != user_id:
            raise CustomException(status_code=HTTP_403_FORBIDDEN, error_code='E305')

        user = self.get_queryset().filter(pk=user_id)
        if not user.exists():
            raise CustomException(status_code=HTTP_404_NOT_FOUND, error_code='E306')
        user = user.get()

        serializer = self.get_serializer_class()

        user_to = serializer(user, data=request.data)
        user_to.is_valid(raise_exception=True)

        user_to.save(updating_user=request.user)

        return Response(user_to.data)

    def destroy(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']

        if not request.user.is_admin:
            raise CustomException(status_code=HTTP_403_FORBIDDEN, error_code='E002')

        user = self.get_queryset().filter(pk=user_id)
        if not user.exists():
            raise CustomException(status_code=HTTP_404_NOT_FOUND, error_code='E306')
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
            raise CustomException(status_code=HTTP_404_NOT_FOUND, error_code='E306')
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
            raise CustomException(status_code=HTTP_404_NOT_FOUND, error_code='E306')
        user = user.get()

        serializer = self.get_serializer_class()
        groups = request.data.get('groups', None)
        if groups is None:
            raise CustomException(status_code=HTTP_400_BAD_REQUEST, error_code='E312')

        try:
            groups_instances = Group.objects.filter(licence_id=user.licence_id, name__in=[g['name'] for g in groups])
        except KeyError as e:
            raise CustomException(status_code=HTTP_400_BAD_REQUEST, error_code='E311')

        if len([g['name'] for g in groups]) != groups_instances.count():
            raise CustomException(status_code=HTTP_400_BAD_REQUEST, error_code='E310')

        user.groups.clear()
        for group in groups_instances:
            user.groups.add(group)
        user.save()

        user_to = serializer(user)

        return Response(user_to.data)


class FooView(ListAPIView):
    def list(self, request, *args, **kwargs):
        return Response({'status': 'UP'})


class CreateResetTokenView(CreateAPIView):
    from rest_framework.permissions import AllowAny
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordTokenSerializer

    def create(self, request, *args, **kwargs):
        form_data = request.data or {}

        serializer = self.get_serializer_class()
        token = serializer(data=form_data)
        token.is_valid(raise_exception=True)

        user = User.objects.filter(email=form_data['email'])
        if not user.exists():
            raise CustomException(status_code=HTTP_400_BAD_REQUEST, error_code='E009', error_message='User with submitted email does not exist')
        user = user.get()

        token_instance = token.save(user=user)

        msg_context = {
            'first_name': user.first_name,
            'reset_page': f'http://localhost:3000/reset?token={token_instance.token}'
        }

        template = render_to_string('reset_password_message.html', context=msg_context)
        send_mail('Reset hasła - Sili',
                  template,
                  'sili20.test@gmail.com',
                  [user.email])

        return Response({'details': 'Reset token created'})


class ValidateResetTokenView(CreateAPIView):
    permission_classes = []
    serializer_class = ResetPasswordTokenSerializer

    def create(self, request, *args, **kwargs):
        form_data = request.data or {}
        if form_data.get('token', None) is None:
            raise CustomException(status_code=HTTP_400_BAD_REQUEST, error_code='E007')

        token_instance = ResetPasswordToken.objects.filter(token=form_data['token'])
        if not token_instance.exists():
            raise CustomException(status_code=HTTP_404_NOT_FOUND, error_code='E008')
        token_instance = token_instance.get()

        return Response(token_instance.token)


class ResetPasswordView(CreateAPIView):
    permission_classes = []
    serializer_class = ResetPasswordSerializer

    def create(self, request, *args, **kwargs):
        form_data = request.data or {}
        serializer = self.get_serializer_class()

        reset_token = serializer(data=form_data)
        reset_token.is_valid(raise_exception=True)

        user = reset_token.save()

        return Response({'details': 'Password changed'})
