from rest_framework_simplejwt.serializers import TokenObtainSlidingSerializer
from rest_framework_simplejwt.views import TokenObtainSlidingView


class CustomTokenSerializer(TokenObtainSlidingSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['licence_id'] = user.licence_id
        token['username'] = user.username
        token['email'] = user.email
        token['is_admin'] = user.is_admin
        token['position'] = user.position
        token['groups'] = [{'id': grp.id, 'name': grp.name} for grp in user.groups.all()]

        return token


class CustomTokenView(TokenObtainSlidingView):
    serializer_class = CustomTokenSerializer

    def post(self, request, *args, **kwargs):
        resp = super().post(request, *args, **kwargs)
        resp.set_cookie('token', resp.data['token'])
        return resp
