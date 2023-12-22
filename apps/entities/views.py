from rest_framework import viewsets

from apps.entities.models import Entity
from apps.entities.serializers import EntitySerializer


class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
