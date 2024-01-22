from django.db import models
from rest_framework import serializers
from groups.models import GroupSerializer
from traits.models import TraitSerializer


class CategoryPet(models.TextChoices):
    MALE = "Male"
    FAMALE = "Female"
    DEFAULT = "Not Informed"


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.CharField()
    group = GroupSerializer()
    traits = TraitSerializer(many=True)


class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        max_length=20, choices=CategoryPet.choices, default=CategoryPet.DEFAULT
    )

    group = models.ForeignKey(
        "groups.Group", on_delete=models.CASCADE, related_name="pets"
    )

    traits = models.ManyToManyField("traits.Trait", related_name="pets")
