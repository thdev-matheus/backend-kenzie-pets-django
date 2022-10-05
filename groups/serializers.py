from rest_framework import serializers


class GroupSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    scientific_name = serializers.CharField(max_length=50)
