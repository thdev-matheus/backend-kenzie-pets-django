from animals.models import Animal
from django.db import IntegrityError
from django.forms import ValidationError
from django.test import TestCase
from groups.models import Group
from traits.models import Trait


class AnimalTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        TRAIT_LIST = ["Peludo", "Grande", "Branco", "Alegre", "Treinado", "Dócil"]

        cls.traits = [
            Trait.objects.get_or_create(name=trait)[0] for trait in TRAIT_LIST
        ]
        cls.group = Group.objects.get_or_create(
            name="Cachorro", scientific_name="Canis Familiaris"
        )[0]

        cls.animal_correct_values = {
            "name": "Rocky",
            "age": 3,
            "weight": 8.2,
            "sex": "Macho",
            "group": cls.group,
        }

        cls.animal_incorrect_values = {
            "name": "Rocky",
            "age": 3,
            "weight": 8.2,
            "sex": "Outro",
            "group": cls.group,
        }

    def testing_Animal_breeding_with_the_correct_data(self):
        animal = Animal.objects.create(**self.animal_correct_values)

        animal.traits.add(*self.traits)

        self.assertIsInstance(animal.group, Group)
        self.assertEqual(animal.group, self.group)
        self.assertIsNotNone(animal.traits)

    def testing_Animal_breeding_with_incorrect_sex(self):

        with self.assertRaises(ValidationError):
            animal = Animal(**self.animal_incorrect_values)
            animal.full_clean()

    def testing_age_to_human_years_conversion_method(self):
        animal = Animal.objects.create(**self.animal_correct_values)

        self.assertIsInstance(animal.convert_dog_age_to_human_years(), float)
        self.assertEqual(animal.convert_dog_age_to_human_years(), 48.60)


class AnimalGroupRelationTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.group_1 = Group.objects.get_or_create(
            name="Cachorro", scientific_name="Canis Familiaris"
        )[0]
        cls.group_2 = Group.objects.get_or_create(
            name="Gato", scientific_name="Felis Catus"
        )[0]

        cls.animal_1_values = {
            "name": "Rocky",
            "age": 3,
            "weight": 8.2,
            "sex": "Macho",
            "group": cls.group_1,
        }

        cls.animal_without_group = {
            "name": "Rocky",
            "age": 3,
            "weight": 8.2,
            "sex": "Macho",
        }

        cls.animal_2_values = {
            "name": "Meg",
            "age": 1,
            "weight": 6.4,
            "sex": "Fêmea",
            "group": cls.group_1,
        }

    def testing_animal_breeding_without_group(self):
        with self.assertRaises(IntegrityError):
            Animal.objects.create(**self.animal_without_group)

    def testing_same_group_assignment_for_two_animals(self):
        animal_1 = Animal.objects.create(**self.animal_1_values)
        animal_2 = Animal.objects.create(**self.animal_2_values)

        self.assertEqual(animal_1.group, animal_2.group)
        self.assertEqual(self.group_1.animals.count(), 2)

    def testing_an_animal_cannot_be_in_two_groups(self):
        animal = Animal.objects.create(**self.animal_1_values)

        self.assertIs(animal.group, self.group_1)
        self.assertNotIn(animal, self.group_2.animals.all())

        animal.group = self.group_2
        animal.save()

        self.assertIs(animal.group, self.group_2)
        self.assertNotIn(animal, self.group_1.animals.all())


class AnimalTraitRelationTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.group_1 = Group.objects.get_or_create(
            name="Cachorro", scientific_name="Canis Familiaris"
        )[0]
        cls.group_2 = Group.objects.get_or_create(
            name="Gato", scientific_name="Felis Catus"
        )[0]

        cls.trait_1 = Trait.objects.get_or_create(name="Peludo")[0]
        cls.trait_2 = Trait.objects.get_or_create(name="Dócil")[0]

        cls.animal_1_values = {
            "name": "Rocky",
            "age": 3,
            "weight": 8.2,
            "sex": "Macho",
            "group": cls.group_1,
        }

        cls.animal_2_values = {
            "name": "Baguera",
            "age": 2,
            "weight": 4.8,
            "sex": "Macho",
            "group": cls.group_2,
        }

        cls.animal_1 = Animal.objects.create(**cls.animal_1_values)
        cls.animal_2 = Animal.objects.create(**cls.animal_2_values)

    def testing_the_same_trait_on_multiple_animals(self):
        self.trait_1.animals.add(self.animal_1, self.animal_2)

        self.assertEqual(self.trait_1.animals.count(), 2)

    def testing_the_same_animal_with_multiple_traits(self):
        self.animal_2.traits.add(self.trait_1, self.trait_2)

        self.assertEqual(self.animal_2.traits.count(), 2)

    def testing_direct_assignment_and_a_many_to_many_relationship(self):
        with self.assertRaisesMessage(
            TypeError,
            "Direct assignment to the forward side of a many-to-many set is prohibited. Use traits.set() instead.",
        ):
            self.animal_1.traits = [self.trait_1, self.trait_2]
