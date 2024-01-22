from django.db import models
from rest_framework import serializers


class TraitSerializer(serializers.Serializer):
    trait_name = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)


class Trait(models.Model):
    id = serializers.IntegerField(read_only=True)
    trait_name = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
