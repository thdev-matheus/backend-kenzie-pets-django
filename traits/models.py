from django.db import models
from django.forms import CharField


# Create your models here.
class Trait(models.Model):
    name = models.CharField(max_length=20, unique=True)
