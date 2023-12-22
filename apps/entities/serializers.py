from rest_framework import serializers
from apps.entities.models import Entity


class EntitySerializer(serializers.ModelSerializer):
    organizations = serializers.PrimaryKeyRelatedField(
        queryset=Entity.objects.filter(
            entity_type=Entity.EntityType.ORGANIZATION), many=True, required=False  # noqa
        )
    parent_entities = serializers.StringRelatedField(many=True)

    class Meta:
        model = Entity
        fields = (
            "uuid", "first_name", "last_name", "email", "entity_type",
            "password", "is_active", "is_system_entity", "organizations",
            "parent_entities"
        )
        read_only_fields = ("is_active", "is_system_entity")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = super().create(validated_data)
        if password is not None:
            instance.set_password(password)
            instance.save()
        return instance
