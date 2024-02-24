from app.models import TimestampedModel
from django.db import models


class Author(TimestampedModel):
    name = models.CharField(max_length=255)


class Book(TimestampedModel):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
