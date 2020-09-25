import jwt
import os
from typing import Optional, Union
from datetime import timedelta, datetime
from cryptography.fernet import Fernet

from user_service.models import UserTO


class JWTService:
    """
    Service providing JWT-related functionalities.
        `refresh_secret` must be base64-encoded 32-byte key
    """
    def __init__(self, private_key: str, public_key: Optional[str], jwt_iss_value: str, algorithm: str,
                 token_lifetime: timedelta, refresh_secret: Union[str, bytes], refresh_token_lifetime: timedelta):
        # specify user's attributes included in JWT
        self._jwt_attributes = ('id', 'username', 'licence_id', 'email', 'is_admin', 'position', 'groups')
        supported_algorithms = {'HS256', 'RS256'}
        if not algorithm in supported_algorithms:
            raise ValueError(
                f'{type(self)} - unsuported algorithm \'{algorithm}\'. Supported - {supported_algorithms}.'
            )
        if algorithm == 'RS256' and public_key is None:
            raise ValueError(
                f'{type(self)} - missing public key for RSA algorithm.'
            )
        elif algorithm == 'HS256':
            public_key = private_key

        # JWT
        self._private_key = private_key
        self._public_key = public_key
        self._iss = jwt_iss_value
        self._alg = algorithm
        self._token_lifetime = token_lifetime
        # Refresh token
        self._refresh_token_enc_dec = Fernet(refresh_secret)
        self._refresh_token_lifetime = refresh_token_lifetime

    def get_user_from_jwt(self, token: str) -> Optional[UserTO]:
        """
        Convert encoded JWT to UserTO. Returns UserTO or None if conversion fails (malformed token, etc.)
        """
        options = {
            'require_exp': True,
            'verify_exp': True,
            'verify_iss': True
        }
        try:
            jwt_payload = jwt.decode(token, self._public_key, issuer=self._iss, algorithms=self._alg, options=options)
            # Remove 'exp' claim from payload
            del jwt_payload['exp']
            return UserTO(**jwt_payload)
        except Exception as err:
            print(err)
            return None

    def create_jwt(self, user: UserTO) -> str:
        """
        Encodes UserTO as JWT. Returns JWT as string.
        """
        # prepare payload with `exp` claim.
        payload = {key: value for key, value in user.as_json().items() if key in self._jwt_attributes}
        payload['exp'] = int((datetime.now() + self._token_lifetime).timestamp())
        payload['iss'] = self._iss

        token = jwt.encode(payload, self._private_key, algorithm=self._alg)
        return token.decode()

    def create_refresh_token(self, token: str) -> str:
        """
        Creates refresh token for JWT.
        """
        token_as_bytes = token.encode()
        refresh_token = self._refresh_token_enc_dec.encrypt(token_as_bytes)
        return refresh_token.decode()

    def validate_refresh_token(self, refresh_token: str) -> Optional[UserTO]:
        """
        Validates refresh token and returns UserTO or None if validation fails.
        """
        refresh_token_as_bytes = refresh_token.encode()
        token = self._refresh_token_enc_dec.decrypt(refresh_token_as_bytes)
        payload = jwt.decode(token, verify=False)
        exp_claim = payload.get('exp', None)
        if exp_claim is None or datetime.fromtimestamp(exp_claim) < datetime.now() - self._refresh_token_lifetime:
            return None
        else:
            try:
                del payload['exp']
                del payload['iss']
                user_to = UserTO(**payload)
                return user_to
            except Exception as err:
                print(err)
                return None
