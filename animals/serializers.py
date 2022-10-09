from math import log

from groups.serializers import GroupSerializer
from rest_framework import serializers
from traits.serializers import TraitSerializer

from .models import Animal, AnimalSex


class AnimalSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        read_only=True
    )  # write_only pode ser usada para um campo password imagino
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices=AnimalSex.choices, default=AnimalSex.NAO_INFORMADO
    )
    age_in_human_years = serializers.SerializerMethodField(read_only=True)

    # definindo as relações no serializer
    group = GroupSerializer()
    traits = TraitSerializer(many=True)

    def get_age_in_human_years(self, instance: Animal) -> float:
        return instance.convert_dog_age_to_human_years()

    def create(self, validated_data):
        # usando os dados validados tenho acesso ao group e aos traits enviados como objeto, agora instancio eles

        # validação e criação ou atribuição do group. No serializer do group é configurado um get_or_create para não duplicar as entradas no DB
        group_serializer = GroupSerializer(data=validated_data["group"])
        group_serializer.is_valid(raise_exception=True)
        group = group_serializer.save()
        validated_data["group"] = group

        # validação e criação ou atribuição das traits depois coloco dentro de uma lista. No serializer da trait é configurado um get_or_create para não duplicar as entradas no DB
        traits = []
        for trait in validated_data["traits"]:
            trait_serializer = TraitSerializer(data=trait)
            trait_serializer.is_valid(raise_exception=True)
            new_trait = trait_serializer.save()
            traits.append(new_trait)

        # retiro a chave traits do validated_data porque não é possível atribuir de forma direta uma lista em uma relação N:N mas a lista já está salva no passo anterior
        validated_data.pop("traits")

        # crio o novo animal sem as traits a princípio
        new_animal = Animal.objects.create(**validated_data)

        # adiciono as traits ao novo animal escrevendo também no database
        new_animal.traits.add(*traits)

        # retorno a model do novo animal
        return new_animal

    def update(self, instance, validated_data):
        # faço uma iteração sobre o dict e atualizo os atributos que foram passados
        for key, value in validated_data.items():
            setattr(instance, key, value)

        # salvo a instância já criada no db
        instance.save()

        # retorno a instância
        return instance
