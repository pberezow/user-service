from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_302_FOUND, \
    HTTP_204_NO_CONTENT, HTTP_201_CREATED
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from django.template.loader import render_to_string
from django.core.mail import send_mail

import threading

from user.models import User, ResetPasswordToken
from user.serializers import ResetPasswordTokenSerializer, ResetPasswordSerializer
from user_service.exceptions import InvalidResetToken


def send_email_with_reset_token(serialized_token, user):
    print('Sending email...')
    token_instance = serialized_token.save(user=user)

    msg_context = {
        'first_name': user.first_name,
        'reset_page': f'http://localhost:3000/reset?token={token_instance.token}'
    }

    template = render_to_string('reset_password_message.html', context=msg_context)
    send_mail('Reset hasła - Sili',
              template,
              'sili20.test@gmail.com',
              [user.email])
    print('Email sent')
    return


class CreateResetTokenView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordTokenSerializer

    def create(self, request, *args, **kwargs):
        form_data = request.data or {}

        serializer = self.get_serializer_class()
        token = serializer(data=form_data)
        token.is_valid(raise_exception=True)

        user = User.objects.filter(email=form_data['email'])
        if not user.exists():
            pass
        else:
            user = user.get()
            task = threading.Thread(target=send_email_with_reset_token, args=[token, user])
            task.setDaemon(True)
            task.start()

        return Response({'details': 'Reset token created'})


class ValidateResetTokenView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordTokenSerializer

    def create(self, request, *args, **kwargs):
        form_data = request.data or {}
        if form_data.get('token', None) is None:
            raise InvalidResetToken()

        token_instance = ResetPasswordToken.objects.filter(token=form_data['token'])
        if not token_instance.exists():
            raise InvalidResetToken()
        token_instance = token_instance.get()

        return Response(token_instance.token)


class ResetPasswordView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordSerializer

    def create(self, request, *args, **kwargs):
        form_data = request.data or {}
        serializer = self.get_serializer_class()

        reset_token = serializer(data=form_data)
        try:
            reset_token.is_valid(raise_exception=True)
        except ValidationError as e:
            raise InvalidResetToken()

        user = reset_token.save()

        return Response({'details': 'Password changed'})
