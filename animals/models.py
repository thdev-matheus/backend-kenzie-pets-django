from math import log

from django.db import models


# Create your models here.
class AnimalSex(models.TextChoices):
    MACHO = "Macho"
    FEMEA = "Fêmea"
    NAO_INFORMADO = "Não Informado"


class Animal(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        max_length=15, choices=AnimalSex.choices, default=AnimalSex.NAO_INFORMADO
    )

    group = models.ForeignKey(
        "groups.Group", on_delete=models.CASCADE, related_name="animals"
    )

    traits = models.ManyToManyField("traits.Trait", related_name="animals")

    def convert_dog_age_to_human_years(self) -> float:
        HUMAN_AGE = 16 * log(self.age) + 31

        return round(HUMAN_AGE, 1)
