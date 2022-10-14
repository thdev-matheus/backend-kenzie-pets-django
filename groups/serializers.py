from rest_framework import serializers

from .models import Group


class GroupSerializer(serializers.Serializer):
    # os campos que eu não quero que sejam "cobrados" ao  inserir os dados mas quero que sejam exibidos na saída ds dados eu deixo como read_only, como o id por exemplo, já para os campos que eu desejo que sejam pedido mas que não quero que sejam exibidos na saída, eu marco como write_only, como um campo de password por exemplo.
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=20)
    scientific_name = serializers.CharField(max_length=50)

    def create(self, validated_data):
        return Group.objects.get_or_create(**validated_data)[0]

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
