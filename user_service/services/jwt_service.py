import jwt
from typing import Optional

from user_service.models import UserTO


class JWTService:
    """
    Service providing JWT-related functionalities.
    """
    def __init__(self, jwt_key):
        self._jwt_key = jwt_key
        self._jwt_attributes = ('id', 'username', 'licence_id', 'email', 'is_admin', 'position', 'groups')

    def get_user_from_jwt(self, token: str) -> Optional[UserTO]:
        """
        Convert encoded JWT to UserTO. Returns UserTO or None if conversion fails (malformed token, etc.)
        """
        try:
            jwt_payload = jwt.decode(token, self._jwt_key, algorithms=['HS256'])
            return UserTO(**jwt_payload)
        except Exception:
            return None

    def create_jwt(self, user: UserTO) -> str:
        """
        Encodes UserTO as JWT. Returns JWT as string.
        """
        payload = {key: value for key, value in user.as_dict().items() if key in self._jwt_attributes}
        token = jwt.encode(payload, self._jwt_key, algorithm='HS256')
        return token.decode()
