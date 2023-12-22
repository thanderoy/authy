from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.query import QuerySet

from apps.common.models import AuthyBaseModel


class BaseEntityManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, first_name, last_name, email, entity_type, ):
        pass


class EntityInactiveManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_active=False)


class EntityActiveManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_active=True)


class EntityAllManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter()


class Entity(AuthyBaseModel, AbstractBaseUser):
    class EntityType(models.TextChoices):
        PERSON = "PSN", "Person"
        ORGANIZATION = "ORG", "Organization"

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', )

    # Entity details
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    entity_type = models.CharField(
        choices=EntityType.choices, max_length=3, default=EntityType.PERSON)
    email = models.EmailField(max_length=255, unique=True, blank=False, null=False)

    # Access + Priviledges
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_system_entity = models.BooleanField(default=False)

    # Relationships
    child_entities = models.ManyToManyField(
        "self", through="Relationship", symmetrical=False, related_name="parent_entities")

    # Managers
    objects = EntityActiveManager()
    inactives = EntityInactiveManager()
    all_records = EntityAllManager()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return f"{self.entity_type} - {self.full_name}"


class Relationship(AuthyBaseModel):
    class RelationshipType(models.TextChoices):
        UNDEFINED = "UND", "Undefined"
        EMPLOYMENT = "EMP", "Employment"

    parent = models.ForeignKey(
        Entity, on_delete=models.CASCADE, related_name='parent_relations')
    child = models.ForeignKey(
        Entity, on_delete=models.CASCADE, related_name='child_relations')
    relationship_type = models.CharField(
        RelationshipType.choices, max_length=50, default=RelationshipType.UNDEFINED)

    def __str__(self) -> str:
        return f"{self.relationship_type} - ({self.parent} -> {self.child})"
