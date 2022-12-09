from datetime import datetime
import datetime

from django.db import models
from studios.models import Studio

# Create your models here.
from django.db.models import CASCADE

WEEK_DAY_CODE = {'monday': 0, 'tuesday': 1, 'wednesday': 2,
                 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}


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
    start_time = models.TimeField(default=None, null=True)
    end_time = models.TimeField(default=None, null=True)
    end_date = models.DateField(default=None, null=True)

    def save(self, *args, **kwargs):
        super(Classes, self).save(*args, **kwargs)
        name = self.name
        coach = self.coach
        weekday = self.weekday
        start_time = self.start_time
        end_time = self.end_time
        end_date = self.end_date
        studio = self.studio

        today = datetime.datetime.today()
        week_day_code = WEEK_DAY_CODE[weekday]
        class_date = today + \
                     datetime.timedelta(days=-today.weekday() + week_day_code, weeks=1)
        class_end = self.end_date
        class_start_time = self.start_time
        class_end_time = self.end_time

        class_lst = Class.objects.filter(classes=self)

        if not class_lst.exists():
            print("create")
            print("aaa", type(class_date.date()), "bbb", type(class_end))
            while class_date.date() < class_end:
                new_class = Class(name=name, start_time=class_start_time, end_time=class_end_time, date=class_date,
                                  studio=studio, classes=self, coach=coach)
                new_class.save()
                class_date = class_date + datetime.timedelta(days=7)
        else:
            print("edit")
            altername = name

            if altername is not None:
                for class_inst in class_lst:
                    class_inst.name = altername
                    class_inst.save()

            for class_inst in class_lst:
                class_inst.start_time = start_time
                class_inst.save()

            for class_inst in class_lst:
                class_inst.end_time = end_time
                class_inst.save()

            class_lst.filter(date__gt=end_date).delete()


class Class(models.Model):
    name = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    classes = models.ForeignKey(Classes, on_delete=CASCADE, null=True)
    studio = models.ForeignKey(Studio, on_delete=CASCADE, null=True)
    coach = models.CharField(max_length=50, null=False)
