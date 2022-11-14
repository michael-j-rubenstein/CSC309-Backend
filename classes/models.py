from django.db import models
from accounts.models import User
from studios.models import Studio

# Create your models here.
from django.db.models import SET_NULL


class Keyword(models.Model):
    keyword = models.CharField(max_length=50, null=False)


class Class(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    studio = models.ForeignKey(Studio, on_delete=SET_NULL, null=True)


class Classes(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=200, null=False)
    coach = models.CharField(max_length=50, null=False)
    capacity = models.IntegerField()
    keywords = models.ManyToManyField(Keyword, default=None)
    # weekday = models.CharField(max_length=10, null=False)
    weekday = models.CharField(max_length=10)
    class_lst = models.ManyToManyField(Class, default=None)




