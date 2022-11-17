from django.db import models
from studios.models import Studio

# Create your models here.
from django.db.models import CASCADE


class Keyword(models.Model):
    keyword = models.CharField(max_length=50, null=False)


class Classes(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=200, null=False)
    coach = models.CharField(max_length=50, null=False)
    capacity = models.IntegerField()
    keywords = models.ManyToManyField(Keyword, default=None)
    weekday = models.CharField(max_length=10)
    studio = models.ForeignKey(Studio, on_delete=CASCADE, null=True)


class Class(models.Model):
    name = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    classes = models.ForeignKey(Classes, on_delete=CASCADE, null=True)
    studio = models.ForeignKey(Studio, on_delete=CASCADE, null=True)







