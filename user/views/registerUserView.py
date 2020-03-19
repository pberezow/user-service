from django.db.utils import IntegrityError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_302_FOUND, \
    HTTP_204_NO_CONTENT, HTTP_201_CREATED

from user.serializers import UserDetailsSerializer, CreateUserSerializer
from user_service.permissions import IsAdminUser, CustomIsAuthenticated as IsAuthenticated
from user_service.exceptions import UserAlreadyExists


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
            raise UserAlreadyExists()

        user_to = UserDetailsSerializer(user_instance)

        return Response(user_to.data, status=HTTP_201_CREATED)
