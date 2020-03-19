from datetime import datetime, timedelta
from calendar import timegm
import jwt

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.conf import settings

from user.models import ResetPasswordToken
from user_service.exceptions import InvalidResetToken


class ResetPasswordTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    class Meta:
        signing_key = settings.SIMPLE_JWT['SIGNING_KEY']
        algorithm = settings.SIMPLE_JWT['ALGORITHM']

    def create(self, validated_data):
        user = validated_data['user']

        exp = datetime.now() + timedelta(days=1)
        exp = timegm(exp.utctimetuple())

        token_payload = {
            'id': user.pk,
            'exp': exp
        }
        token = jwt.encode(token_payload, self.Meta.signing_key, algorithm=self.Meta.algorithm).decode('utf-8')
        if hasattr(user, 'token'):
            obj = user.token
            obj.token = token
            obj.save()
        else:
            obj = ResetPasswordToken(user=user, token=token)
            obj.save()

        return obj


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    password = serializers.CharField(max_length=128, required=True, validators=[validate_password])

    def create(self, validated_data):
        token_instance = ResetPasswordToken.objects.filter(token=validated_data['token'])
        if not token_instance.exists():
            raise InvalidResetToken()

        token_instance = token_instance.get()
        user = token_instance.user
        user.set_password(validated_data['password'])
        user.save(update_fields=["password"])
        token_instance.delete()
        return user
