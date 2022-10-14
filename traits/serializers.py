from rest_framework import serializers

from .models import Trait


class TraitSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=20)

    def create(self, validated_data):
        trait, _ = Trait.objects.get_or_create(**validated_data)
        return trait

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
