# Generated by Django 4.1.2 on 2022-10-05 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("animals", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Trait",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20, unique=True)),
                (
                    "animals",
                    models.ManyToManyField(related_name="traits", to="animals.animal"),
                ),
            ],
        ),
    ]
