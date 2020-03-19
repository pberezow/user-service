from rest_framework import serializers
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.password_validation import validate_password

from group.serializers import GroupSerializer
from user.models import User
from group.models import Group


class CreateUserSerializer(serializers.Serializer):
    """
    Used in /register endpoint
    """
    licence_id = serializers.IntegerField(required=True)
    username = serializers.CharField(max_length=150, required=True, validators=[UnicodeUsernameValidator()],
                                     allow_blank=False, allow_null=False)
    password = serializers.CharField(max_length=128, required=True, validators=[validate_password])
    is_admin = serializers.BooleanField(default=False)
    first_name = serializers.CharField(max_length=30, allow_blank=True, required=False)
    last_name = serializers.CharField(max_length=150, allow_blank=True, required=False)
    email = serializers.EmailField(required=True)
    phone_number = serializers.CharField(max_length=12, allow_blank=True, required=False)
    address = serializers.CharField(max_length=100, allow_blank=True, required=False)
    position = serializers.CharField(max_length=30, allow_blank=True, required=False)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    Used in details view + update/retrieve user data
    /
    /<id>
    """
    groups = GroupSerializer(required=False, many=True)

    class Meta:
        model = User
        exclude = ['is_staff', 'date_joined', 'last_login', 'is_superuser', 'user_permissions', 'password']
        read_only_fields = ['is_staff', 'date_joined', 'last_login', 'is_superuser', 'licence_id', 'username', 'id',
                            'groups']
        # extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def update(self, instance, validated_data):
        updating_user = validated_data.get('updating_user', None)

        if not updating_user:
            raise Exception('This error should never occur!')

        if updating_user.is_admin:
            instance.is_admin = validated_data.get('is_admin', instance.is_admin)
            instance.first_name = validated_data.get('first_name', instance.first_name)
            instance.last_name = validated_data.get('last_name', instance.last_name)
            instance.email = validated_data.get('email', instance.email)
            instance.address = validated_data.get('address', instance.address)
            instance.position = validated_data.get('position', instance.position)
            instance.is_active = validated_data.get('is_active', instance.is_admin)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)

        instance.save()
        return instance


class UserSimpleSerializer(serializers.ModelSerializer):
    """
    Used in users list view for non admin users (and admin?)
    """
    # include context={'request': request} when creating serializer
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'position']


class UserSetPasswordSerializer(serializers.ModelSerializer):
    """
    Used in SetUsersPasswordView
    /<id>/password
    """
    old_password = serializers.CharField(max_length=128, required=False)

    class Meta:
        model = User
        fields = ['password', 'old_password']
        extra_kwargs = {'password': {'write_only': True, 'required': True, 'validators': [validate_password]}}

    def update(self, instance, validated_data):
        updating_user = validated_data.get('updating_user', None)
        if not updating_user:
            raise Exception('This error should never occur! Updating user not provided in save() method.')

        if updating_user.is_admin:
            instance.set_password(validated_data['password'])
        else:
            if validated_data.get('old_password', False):
                if instance.check_password(validated_data['old_password']):
                    instance.set_password(validated_data['password'])

        instance.save()
        return instance


class UserSetGroupSerializer(serializers.ModelSerializer):
    """
    Used in set user's groups endpoint
    NOT WORKING - done workaround in user.views - SetUserGroupsView
    """
    groups = GroupSerializer(many=True, read_only=False)

    class Meta:
        model = User
        exclude = ['is_staff', 'date_joined', 'last_login', 'is_superuser', 'user_permissions', 'password']
        read_only_fields = ['is_staff', 'date_joined', 'last_login', 'is_superuser', 'licence_id', 'username', 'id']

    def update(self, instance, validated_data):
        # TODO: fix this serializer and use it when setting user's permissions
        groups_data = validated_data.get('groups', [])
        print(groups_data)
        if not groups_data:
            return instance

        groups = Group.objects.filter(licence_id=instance.licence_id, name__in=[g['name'] for g in groups_data])

        instance.groups = groups
        instance.save()

        return instance
