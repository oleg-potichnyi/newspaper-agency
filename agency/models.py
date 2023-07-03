from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


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

    def get_absolute_url(self) -> str:
        return reverse("agency:redactor-detail", kwargs={"pk": self.pk})


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
