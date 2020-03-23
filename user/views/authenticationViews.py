from rest_framework_simplejwt.views import TokenObtainSlidingView, TokenRefreshSlidingView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_302_FOUND, \
    HTTP_204_NO_CONTENT, HTTP_201_CREATED
from rest_framework import exceptions
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import AllowAny

from user_service.permissions import CustomIsAuthenticated as IsAuthenticated
from user_service.exceptions import InvalidJWT, InvalidCredentials
from user.serializers import CustomTokenSerializer, CustomTokenRefreshSerializer


class CustomTokenView(TokenObtainSlidingView):
    serializer_class = CustomTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.ValidationError as e:
            raise InvalidCredentials()
        except TokenError as e:
            # raise InvalidToken(e.args[0])
            raise InvalidCredentials()

        resp = Response(serializer.validated_data, status=status.HTTP_200_OK)
        resp.set_cookie('token', resp.data['token'])
        return resp


class CustomTokenRefreshView(TokenRefreshSlidingView):
    serializer_class = CustomTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.ValidationError as e:
            raise InvalidJWT()
        except TokenError as e:
            # raise InvalidToken(e.args[0])
            raise InvalidJWT()

        resp = Response(serializer.validated_data, status=status.HTTP_200_OK)
        resp.set_cookie('token', resp.data['token'])
        return resp


class LogoutView(RetrieveAPIView):  # GET
    """
    Logout - remove token cookie
    """
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        resp = Response()
        resp.delete_cookie('token')
        return resp
