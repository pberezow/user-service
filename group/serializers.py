from rest_framework import serializers
from rest_framework import exceptions
from group.models import Group
from user_service.exceptions import validation_errors_map, ValidationError


class GroupSerializer(serializers.ModelSerializer):
    """
    Used in groups endpoints
    """
    class Meta:
        model = Group
        fields = ['name', 'licence_id']
        extra_kwargs = {'licence_id': {'required': False}}

    def create(self, validated_data):
        group = Group(**validated_data)
        group.save()
        return group

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        return instance

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
