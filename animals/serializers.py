from groups.models import Group
from groups.serializers import GroupSerializer
from rest_framework import serializers
from traits.models import Trait
from traits.serializers import TraitSerializer

from .models import Animal, AnimalSex


class AnimalSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices=AnimalSex.choices, default=AnimalSex.NAO_INFORMADO
    )
    age_in_human_years = serializers.SerializerMethodField(read_only=True)

    group = GroupSerializer()
    traits = TraitSerializer(many=True)

    def get_age_in_human_years(self, instance: Animal) -> float:
        return instance.convert_dog_age_to_human_years()

    def create(self, validated_data):

        group, _ = Group.objects.get_or_create(**validated_data["group"])
        traits = [
            Trait.objects.get_or_create(**trait)[0]
            for trait in validated_data["traits"]
        ]

        validated_data["group"] = group
        validated_data.pop("traits")

        animal = Animal.objects.create(**validated_data)
        animal.traits.add(*traits)

        return animal

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
