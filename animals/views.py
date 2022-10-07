from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response, status

from animals.serializers import AnimalSerializer

from .models import Animal
from .utils import validate_fields_request


# criando uma classe para cada nível de endpoint
# api/
class AnimalView(APIView):
    def get(self, request) -> Response:
        animals = Animal.objects.all()

        serialize = AnimalSerializer(animals, many=True)

        return Response(serialize.data)

    def post(self, request) -> Response:
        serializer = AnimalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_animal = serializer.save()
        animal = AnimalSerializer(new_animal)

        return Response(animal.data, status.HTTP_201_CREATED)


class AnimalParamsView(APIView):
    def get(self, request, animal_id: int) -> Response:
        animal = get_object_or_404(Animal, id=animal_id)

        serializer = AnimalSerializer(animal)

        return Response(serializer.data)

    def patch(self, request, animal_id: int) -> Response:
        animal = get_object_or_404(Animal, id=animal_id)

        no_valid_request = validate_fields_request(request.data)
        if no_valid_request:
            return Response(no_valid_request, status.HTTP_400_BAD_REQUEST)

        serializer = AnimalSerializer(animal, request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)
