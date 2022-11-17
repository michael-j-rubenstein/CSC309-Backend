from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Class, Classes, Keyword
from studios.models import Studio
from accounts.models import CustomUser as User
import json
from datetime import datetime
import datetime
from rest_framework.decorators import api_view



WEEK_DAY_CODE = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}

# Create your views here.
# def ListClassView(request, id):
#     if request == 'GET':
#         studio_id = id
#         studio = Studio.objects.get(id=studio_id)


@api_view(['POST'])
@csrf_exempt
def CreateClasses(request, id):
    if request.method == "POST":
        if not request.user.is_superuser:
            return HttpResponse("Not Admin", status=403)
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

        new_classes = Classes(name=name, description=description, coach=coach, capacity=capacity, weekday=weekday, studio=studio)
        new_classes.save()

        for keyword in keywords:
            try:
                keyword_instance = Keyword.objects.get(keyword=keyword)
            except Keyword.DoesNotExist:
                keyword_instance = None

            if keyword_instance:
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
        new_classes.save()

        while class_date < class_end:
            new_class = Class(name=name, start_time=class_start_time, end_time=class_end_time, date=class_date,
                              studio=studio, classes=new_classes)
            new_class.save()
            # new_classes.class_lst.add(new_class)
            class_date = class_date + datetime.timedelta(days=7)

        new_classes.save()

        return HttpResponse("Class Created Successfully")


@api_view(["POST"])
@csrf_exempt
def RemoveClass(request):
    if request.method == "POST":
        class_info = json.loads(request.body)
        name = class_info.get('name')
        date = class_info.get('date')
        class_to_remove = Class.objects.filter(name=name, date=date)
        class_to_remove.delete()
        return HttpResponse("Class Cancelled Successfully!")


@api_view(["POST"])
@csrf_exempt
def RemoveClasses(request):
    if request.method == "POST":
        class_info = json.loads(request.body)
        name = class_info.get('name')
        class_to_remove = Classes.objects.filter(name=name)
        class_to_remove.delete()
        return HttpResponse("Classes Cancelled Successfully!")


@api_view(["GET"])
@csrf_exempt
def ListClasses(request, id):
    if request.method == "GET":
        studio = Studio.objects.get(id=id)
        now = datetime.now()
        order_class = Class.objects.filter(studio=studio).order_by('date', 'start_time')
        data = []
        for class_inst in order_class:
            print(class_inst.date, now.date(), class_inst.start_time, now.time())
            if class_inst.date > now.date():
                print("here")
                class_info = {"name": class_inst.name, "start_time": class_inst.start_time,
                              "end_time": class_inst.end_time, "date": class_inst.date}
                data.append(class_info)

        return JsonResponse(data, safe=False)


@api_view(["POST"])
@csrf_exempt
def EnrollClasses(request, id):
    if request.method == "POST":
        studio = Studio.objects.get(id=id)
        data = json.loads(request.body)
        classes = Classes.objects.get(studio=studio, name=data.get("classname"))
        if classes.capacity == 0:
            return HttpResponse("Enrolling failed! The class is full!")
        else:
            username = data.get("username")
            user = User.objects.get(username=username)
            if user.subscription != 1:
                return HttpResponse("Need subscribe first to enroll the class!")
            elif user.subscription == 1:
                new_cap = classes.capacity - 1
                classes.capacity = new_cap
                user.classes.add(classes)
                class_lst = Class.objects.filter(classes=classes)
                for class_inst in class_lst:
                    user.class_lst.add(class_inst.id)
                return HttpResponse("Enroll in class successfully!")


@api_view(["POST"])
@csrf_exempt
def DeleteClasses(request):
    if request.method == "POST":
        info = json.loads(request.body)
        user = User.objects.get(username=info.get("username"))
        user_classes_lst = user.classes_lst
        classes = Classes.objects.get(name=info.get("classes"))
        user_classes_lst.remove(classes)
        new_cap = classes.capacity + 1
        classes.capacity = new_cap
        return HttpResponse("Class dropped successfully!")


@api_view(["POST"])
@csrf_exempt
def DeleteClass(request):
    if request.method == "POST":
        info = json.loads(request.body)
        user = User.objects.get(username=info.get("username"))
        user_class_lst = user.class_lst
        date_raw = info.get("date")
        print(date_raw)
        print(date_raw["year"], date_raw["month"], date_raw["day"])
        year = date_raw["year"]
        month = date_raw["month"]
        day = date_raw["day"]
        class_date = datetime.date(year, month, day)
        class_to_delete = Class.objects.get(name=info.get("class"), date=class_date)
        user_class_lst.remove(class_to_delete)
        return HttpResponse("Class session delete successfully!")


@api_view(["GET"])
@csrf_exempt
def UserSchedule(request):
    if request.method == "GET":
        info = json.loads(request.body)
        user = User.objects.get(username=info.get("username"))
        now = datetime.datetime.now()
        print(request.user)
        order_class = user.class_lst.order_by('date', 'start_time')
        data = []
        for class_inst in order_class:
            if class_inst.date > now.date():
                class_info = {"name": class_inst.name, "start_time": class_inst.start_time,
                              "end_time": class_inst.end_time, "date": class_inst.date}
                data.append(class_info)

        return JsonResponse(data, safe=False)












