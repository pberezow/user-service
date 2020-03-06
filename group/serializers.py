from rest_framework import serializers
from group.models import Group


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
