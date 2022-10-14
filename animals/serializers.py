from groups.models import Group
from groups.serializers import GroupSerializer
from rest_framework import serializers
from traits.models import Trait
from traits.serializers import TraitSerializer

from .models import Animal, AnimalSex


# O serializer é usado para validação de dados e também para controle de saída dos dados funcionando como uma especie de "filtro" por onde os dados entram, são validados, aramazenados, atualizados e são exibidos.
class AnimalSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        max_length=50
    )  # Charfield na model é obrigatório passar o max_length, no serializer não. em compensação no serializer não existe o TextField. "Tudo" é CharField
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    # Na model usamos um CharField com um argumento choices para o campo de escolhas
    # já no serializer usamos o ChoiceField e não precisaos passar o max_length
    sex = serializers.ChoiceField(
        choices=AnimalSex.choices, default=AnimalSex.NAO_INFORMADO
    )

    # campo que não existe na model e que não é persistido no banco e vai ser o retorno de um étodo do serializer. Marcamos como apenas leitura
    age_in_human_years = serializers.SerializerMethodField(read_only=True)

    # mapeamos a relação e dependendo da regra de negócio podemos marcar como read_only ou write_only
    group = GroupSerializer()

    # ao mapear uma relação N:N colocamos um argumento "many=True" pra que o serializer entenda que será várias instâncias de serializer.
    traits = TraitSerializer(many=True)

    # método de instância que definiá o valor do campo que não existe na model. podemos definir o nome do método quando configuramos o campo. se não fizermos isso devemos nomear o método como get_<nome_do_campo>
    def get_age_in_human_years(self, instance: Animal) -> float:
        return instance.convert_dog_age_to_human_years()

    # sobreescevendo o método create
    def create(self, validated_data):

        # como definimos que os campos group e traits serão de outros serializers, ao chamar o is_valid do serializer de animais os valores de group e traits já são validados em seus respectivos serializers também assim podemos apenas persistir no banco de dados

        # pega do banco ou cria o grupo com os dados que vem no validated_data na posição group
        group, _ = Group.objects.get_or_create(**validated_data["group"])

        # list comprehension de pega do banco ou cria as traits com os dados que vem no validated_data
        # precisamos guardar aqui para poder vincular depois ao animal criado
        traits = [
            Trait.objects.get_or_create(**trait)[0]
            for trait in validated_data["traits"]
        ]

        # sobreescreve o validated_data["group"] para que tenha uma instância de Group (no momento tem apenas um ordered_dict validado) e possa ser persistido corretamente no banco
        validated_data["group"] = group

        # retiro a chave "traits" do validated_data porque não se pode atribuir diretamente numa relação N:N
        validated_data.pop("traits")

        # persisto no banco o animal SEM as traits
        animal = Animal.objects.create(**validated_data)

        # Vinculo as traits ao animal devidamente, obedecendo a regra da relação N:N
        animal.traits.add(*traits)

        # retorno o animal
        return animal

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
