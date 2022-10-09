from django.db import IntegrityError
from django.test import TestCase
from groups.models import Group


class GroupTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.group_name = "Cachorro"
        cls.group_scientific_name = "Canis Familiaris"

    def testing_the_creation_of_a_group_with_correct_data(self):
        group = Group.objects.create(
            name=self.group_name, scientific_name=self.group_scientific_name
        )

        self.assertEqual(group.name, self.group_name)
        self.assertEqual(group.scientific_name, self.group_scientific_name)

    def testing_the_creation_of_two_groups_with_the_same_name(self):
        Group.objects.create(
            name=self.group_name, scientific_name=self.group_scientific_name
        )

        with self.assertRaises(IntegrityError):
            Group.objects.create(
                name=self.group_name, scientific_name=self.group_scientific_name
            )
