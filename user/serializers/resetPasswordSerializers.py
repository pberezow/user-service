from datetime import datetime, timedelta
from calendar import timegm
import jwt

from rest_framework import serializers
from rest_framework import exceptions
from django.contrib.auth.password_validation import validate_password
from django.conf import settings

from user.models import ResetPasswordToken
from user_service.exceptions import validation_errors_map, InvalidResetToken, ValidationError


class ResetPasswordTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    class Meta:
        signing_key = settings.SIMPLE_JWT['SIGNING_KEY']
        algorithm = settings.SIMPLE_JWT['ALGORITHM']

    def is_valid(self, raise_exception=False):
        try:
            r = super().is_valid(raise_exception)
        except exceptions.ValidationError as e:
            errors = []
            for k, v in e.detail.items():
                # error = validation_errors_map[k]
                error = validation_errors_map.get(k, None)  # can be 'non_field_errors' ex. when unique_together
                if error is None:
                    raise ValidationError()
                errors.append(ValidationError(*error))
            raise ValidationError(error_code=errors)
        return r

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
    token = serializers.CharField(required=True, max_length=600)
    password = serializers.CharField(max_length=128, required=True, validators=[validate_password])

    def is_valid(self, raise_exception=False):
        try:
            r = super().is_valid(raise_exception)
        except exceptions.ValidationError as e:
            errors = []
            for k, v in e.detail.items():
                # error = validation_errors_map[k]
                error = validation_errors_map.get(k, None)  # can be 'non_field_errors' ex. when unique_together
                if error is None:
                    raise ValidationError()
                errors.append(ValidationError(*error))
            raise ValidationError(error_code=errors)
        return r

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
