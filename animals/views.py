from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status

from animals.serializers import AnimalSerializer

from .models import Animal
from .utils import validate_fields_request


class AnimalView(APIView):
    def get(self, request: Request) -> Response:
        # pego todos os animais do banco de dados
        animals = Animal.objects.all()

        # uso o serializer para controlar os dados de saida passando o many como true para o serializer identificar que será um iterável, não preciso validar porque estou passando as instâncias.
        serialize = AnimalSerializer(animals, many=True)

        return Response(serialize.data)

    def post(self, request: Request) -> Response:
        # pego o que virá da rrequisição e instancio no serializer para validar os dados
        serializer = AnimalSerializer(data=request.data)

        # a validação já vai validar o group  as traits por causa da config no serializer
        serializer.is_valid(raise_exception=True)

        # chamo o método para criar o animal e persistir no banco
        serializer.save()

        # retorna os dados validados com status 201
        return Response(serializer.data, status.HTTP_201_CREATED)


class AnimalParamsView(APIView):
    def get(self, request: Request, animal_id: int) -> Response:
        # método pega ou lança um erro 404 do shortcuts do django passando como argumento a model e a chave que irá ser usada para capturar o animal do DB
        animal = get_object_or_404(Animal, id=animal_id)

        # serializo os dados para controlar a saída, como estou passando a instância o serializer já presume que esteja validado e não pede para validar
        serializer = AnimalSerializer(animal)

        # retorna os dados serializados com status 200
        return Response(serializer.data)

    def patch(self, request: Request, animal_id: int) -> Response:
        # método pega ou lança um erro 404 do shortcuts do django passando como argumento a model e a chave que irá ser usada para capturar o animal do DB
        animal = get_object_or_404(Animal, id=animal_id)

        # método de um pacote criado que valida se na request o cliente tentou atualizar as traits ou os groups ou o sex do animal. retorna um dict
        no_valid_request = validate_fields_request(request.data)

        # se o dict não estiver vazio retorna um status 400 com o dict que terá as chaves indicando os erros
        if no_valid_request:
            return Response(no_valid_request, status.HTTP_400_BAD_REQUEST)

        # serializo os dados para validar as entradas só que dessa vez passando o argumento "partial=True" por se tratar do patch.
        # também devo passar a instância EEEEEE os dados para atualizar
        serializer = AnimalSerializer(animal, request.data, partial=True)

        # valido os dados
        serializer.is_valid(raise_exception=True)

        # como eu passei a instância e os dados pra inserir o drf vai entender que deve chamar o metodo update do serializer ao invés do create
        serializer.save()

        # retorna o animal com os dados validados e atualizados no banco e o status 200
        return Response(serializer.data)

    def delete(self, request: Request, animal_id: int) -> Response:
        # método pega ou lança um erro 404 do shortcuts do django passando como argumento a model e a chave que irá ser usada para capturar o animal do DB
        animal = get_object_or_404(Animal, id=animal_id)

        # deleta a instância do banco
        animal.delete()

        # retorna o status 204 sem body para p cliente
        return Response(status=status.HTTP_204_NO_CONTENT)
