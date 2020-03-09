from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainSlidingSerializer, TokenRefreshSlidingSerializer, SlidingToken
from rest_framework_simplejwt.views import TokenObtainSlidingView, TokenRefreshSlidingView
from rest_framework_simplejwt.settings import api_settings
from django.utils.translation import ugettext_lazy as _

from user.models import User

import jwt


def set_additional_payload(token, user):
    """
    Set custom token's claims.
    """
    token['licence_id'] = user.licence_id
    token['username'] = user.username
    token['email'] = user.email
    token['is_admin'] = user.is_admin
    token['position'] = user.position
    token['groups'] = [{'id': grp.id, 'name': grp.name} for grp in user.groups.all()]
    return token


class CustomTokenSerializer(TokenObtainSlidingSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token = set_additional_payload(token, user)

        return token


class CustomTokenView(TokenObtainSlidingView):
    serializer_class = CustomTokenSerializer

    def post(self, request, *args, **kwargs):
        resp = super().post(request, *args, **kwargs)
        resp.set_cookie('token', resp.data['token'])
        return resp


class CustomJWTDecoder:
    """
    Class used when decoding and verifying sliding token on refresh endpoint.
    Used in CustomTokenRefreshSerializer for signature validations.

    - workaround of https://github.com/davesque/django-rest-framework-simplejwt/issues/154
    """
    algorithm = api_settings.ALGORITHM
    # if alg == 'HS***' then SIGNING_KEY == VERIFYING_KEY
    verifying_key = api_settings.VERIFYING_KEY if api_settings.VERIFYING_KEY else api_settings.SIGNING_KEY
    audience = api_settings.AUDIENCE
    issuer = api_settings.ISSUER

    def decode(self, token, verify=True):
        """
        Performs a validation of the given token and returns its payload
        dictionary.

        Raises a `TokenError` if the token is malformed, if its signature check fails.
        """
        try:
            # Default sliding token verification checks exp claim, which can be expired on refresh endpoint,
            # it should skip exp claim and verify refresh_exp instead.
            # This decoder provides all necessary validation for JWT(signature, jti, etc.) while skipping exp,
            # but it doesn't validate refresh_exp - it will be validate later in CustomTokenRefreshSerializer class.
            return jwt.decode(token, self.verifying_key, algorithms=[self.algorithm], verify=verify,
                              audience=self.audience, issuer=self.issuer,
                              options={'verify_aud': self.audience is not None,
                                       # 'verify_iss': self.issuer is not None,
                                       'verify_exp': False})
        except jwt.exceptions.InvalidTokenError:
            raise TokenError(_('Token is invalid or expired'))
        except jwt.exceptions.InvalidSignatureError:
            raise TokenError(_('Token is invalid or expired'))


jwtDecoder = CustomJWTDecoder()


class CustomTokenRefreshSerializer(TokenRefreshSlidingSerializer):

    def validate(self, attrs):
        # Check if signature and jti is correct
        jwtDecoder.decode(attrs['token'])

        # Decode token without validation - it was validated before
        token = SlidingToken(attrs['token'], verify=False)

        # Check that the timestamp in the "refresh_exp" claim has not passed
        token.check_exp(api_settings.SLIDING_TOKEN_REFRESH_EXP_CLAIM)

        # Validate if user exists in database and if is_active
        user = User.objects.filter(pk=token[api_settings.USER_ID_CLAIM])
        if not user.exists():
            raise TokenError(_('Token is invalid or expired'))

        user = user.get()
        if not user.is_active:
            raise TokenError(_('Token is invalid or expired'))

        # Swap payload (some user's)
        token = set_additional_payload(token, user)

        # Update the "exp" claim
        token.set_exp()

        return {'token': str(token)}


class CustomTokenRefreshView(TokenRefreshSlidingView):
    serializer_class = CustomTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        resp = super().post(request, *args, **kwargs)
        resp.set_cookie('token', resp.data['token'])
        return resp
