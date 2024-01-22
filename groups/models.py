from django.db import models
from rest_framework import serializers


class GroupSerializer(serializers.Serializer):
    scientific_name = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)


class Group(models.Model):
    id = serializers.IntegerField(read_only=True)
    scientific_name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
