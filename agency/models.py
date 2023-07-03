from django.contrib.auth.models import AbstractUser
from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField()

    class Meta:
        verbose_name = "redactor"
        verbose_name_plural = "redactors"

    def __str__(self) -> str:
        return f"{self.username} {self.first_name} {self.last_name}"


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateField(
        auto_now_add=True, verbose_name="Date Published"
    )
    topic = models.ManyToManyField(Topic, related_name="newspaper")
    publishers = models.ManyToManyField(Redactor, related_name="newspaper")

    def __str__(self) -> str:
        return self.title


Redactor._meta.get_field("groups").remote_field.related_name =\
    "redactor_groups"
Redactor._meta.get_field("user_permissions").remote_field.related_name =\
    "redactor_set"
