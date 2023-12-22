from rest_framework import serializers
from apps.entities.models import Entity


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = (
            "first_name", "last_name", "email", "entity_type", "password",
            "is_active",
        )
        read_only_fields = ("is_active",)
