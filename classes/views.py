from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, FormView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Class, Classes, Keyword
from studios.models import Studio
import json
import datetime

WEEK_DAY_CODE = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}

# Create your views here.
# def ListClassView(request, id):
#     if request == 'GET':
#         studio_id = id
#         studio = Studio.objects.get(id=studio_id)


@csrf_exempt
def CreateClasses(request, id):
    # if request.method == "POST" and request.user.is_superuser:
    if request.method == "POST":
        studio_id = id
        studio = Studio.objects.get(id=studio_id)
        classes_info = json.loads(request.body)
        print("body", classes_info)
        name = classes_info.get('name')
        description = classes_info.get('description')
        coach = classes_info.get('coach')
        capacity = int(classes_info.get('capacity'))
        keywords = classes_info.get('keywords')
        weekday = classes_info.get('weekday')
        start_time = classes_info.get('start_time')
        end_time = classes_info.get('end_time')
        end_date = classes_info.get('end_date')

        new_classes = Classes(name=name, description=description, coach=coach, capacity=capacity, weekday=weekday)
        new_classes.save()

        for keyword in keywords:
            keyword_instance = Keyword.objects.get(keyword=keyword)

            if keyword_instance is not None:
                new_classes.keywords.add(keyword_instance.id)
            else:
                new_keyword = Keyword(keyword=keyword)
                new_keyword.save()
                new_classes.keywords.add(new_keyword)

        today = datetime.date.today()
        week_day_code = WEEK_DAY_CODE[weekday]
        class_date = today + datetime.timedelta(days=-today.weekday() + week_day_code, weeks=1)
        class_end = datetime.date(end_date["year"], end_date["month"], end_date["day"])
        class_start_time = datetime.time(start_time['hour'], start_time['minute'])
        class_end_time = datetime.time(end_time['hour'], end_time['minute'])

        while class_date < class_end:
            new_class = Class(start_time=class_start_time, end_time=class_end_time, date=class_date, studio=studio)
            new_class.save()
            new_classes.class_lst.add(new_class)
            class_date = class_date + datetime.timedelta(days=7)

        new_classes.save()

        return HttpResponse("Class Created Successfully")






