from django.db import IntegrityError
from django.forms import ValidationError
from django.test import TestCase
from traits.models import Trait


class TraitTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.trait_name = "Protetor"

    def testing_the_creation_of_a_trait_with_correct_data(self):
        trait = Trait.objects.create(name=self.trait_name)

        self.assertEqual(trait.name, self.trait_name)

    def testing_the_creation_of_two_traits_with_the_same_name(self):
        Trait.objects.create(name=self.trait_name)

        with self.assertRaises(IntegrityError):
            Trait.objects.create(name=self.trait_name)

    def testing_the_creation_of_a_trait_with_a_name_longer_than_20_characters(self):
        with self.assertRaises(ValidationError):
            trait = Trait(name="Inconstitucionalissimamente")
            trait.full_clean()
