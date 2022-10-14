from django.db import models


# crio a model traits herdando de models.Model
class Trait(models.Model):
    name = models.CharField(max_length=20, unique=True)
