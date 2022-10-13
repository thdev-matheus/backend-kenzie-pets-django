from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status

from animals.serializers import AnimalSerializer

from .models import Animal
from .utils import validate_fields_request


class AnimalView(APIView):
    def get(self, request: Request) -> Response:
        animals = Animal.objects.all()

        serialize = AnimalSerializer(animals, many=True)

        return Response(serialize.data)

    def post(self, request: Request) -> Response:
        serializer = AnimalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class AnimalParamsView(APIView):
    def get(self, request: Request, animal_id: int) -> Response:
        animal = get_object_or_404(Animal, id=animal_id)

        serializer = AnimalSerializer(animal)

        return Response(serializer.data)

    def patch(self, request: Request, animal_id: int) -> Response:
        animal = get_object_or_404(Animal, id=animal_id)

        no_valid_request = validate_fields_request(request.data)
        if no_valid_request:
            return Response(no_valid_request, status.HTTP_400_BAD_REQUEST)

        serializer = AnimalSerializer(animal, request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)

    def delete(self, request: Request, animal_id: int) -> Response:
        animal = get_object_or_404(Animal, id=animal_id)

        animal.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
