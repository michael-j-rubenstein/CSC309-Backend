from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Class, Classes, Keyword
from studios.models import Studio
import stripe
import time

from accounts.models import Users as User
import json
from datetime import datetime
import datetime
from rest_framework.decorators import api_view
from subscriptions.models import StripeUser, StripeUserLog

WEEK_DAY_CODE = {'monday': 0, 'tuesday': 1, 'wednesday': 2,
                 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}


@api_view(['POST'])
@csrf_exempt
def CreateClasses(request, id):
    if request.method == "POST":
        if not request.user.is_superuser:
            return HttpResponse("Not Admin", status=403)
        studio_id = id
        studio = Studio.objects.get(id=studio_id)
        if studio is None:
            return HttpResponse("No studio found", status=404)
        classes_info = json.loads(request.body)
        name = classes_info.get('name')
        if Classes.objects.filter(name=name).exists():
            return HttpResponse("This class name already exists")

        description = classes_info.get('description')
        coach = classes_info.get('coach')
        capacity = int(classes_info.get('capacity'))
        keywords = classes_info.get('keywords')
        weekday = classes_info.get('weekday')
        start_time = classes_info.get('start_time')
        end_time = classes_info.get('end_time')
        end_date = classes_info.get('end_date')

        new_classes = Classes(name=name, description=description,
                              coach=coach, capacity=capacity, weekday=weekday, studio=studio)
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
        class_date = today + \
                     datetime.timedelta(days=-today.weekday() + week_day_code, weeks=1)
        class_end = datetime.date(
            end_date["year"], end_date["month"], end_date["day"])
        class_start_time = datetime.time(
            start_time['hour'], start_time['minute'])
        class_end_time = datetime.time(end_time['hour'], end_time['minute'])
        new_classes.save()

        while class_date < class_end:
            new_class = Class(name=name, start_time=class_start_time, end_time=class_end_time, date=class_date,
                              studio=studio, classes=new_classes, coach=coach)
            new_class.save()
            # new_classes.class_lst.add(new_class)
            class_date = class_date + datetime.timedelta(days=7)

        new_classes.save()

        return HttpResponse("Class Created Successfully")


@api_view(['POST'])
@csrf_exempt
def EditClasses(request, id):
    if request.method == "POST":
        if not request.user.is_superuser:
            return HttpResponse("Not Admin", status=403)
        studio_id = id
        studio = Studio.objects.get(id=studio_id)
        if studio is None:
            return HttpResponse("No studio found", status=404)
        classes_info = json.loads(request.body)
        name = classes_info.get('name')
        description = classes_info.get('description')
        coach = classes_info.get('coach')
        capacity = int(classes_info.get('capacity'))

        classes = Classes.objects.get(studio=studio, name=name)
        class_lst = Class.objects.get(studio=studio, name=name)

        if description is not None:
            classes.description = description

        if coach is not None:
            classes.coach = coach
            for class_inst in class_lst:
                class_inst.coach = coach

        if capacity is not None:
            classes.capacity = capacity

        classes.save()

        return HttpResponse("Edit Class Successfully!")


@api_view(["POST"])
@csrf_exempt
def RemoveClass(request):
    if request.method == "POST":
        if not request.user.is_superuser:
            return HttpResponse("Not Admin", status=403)
        class_info = json.loads(request.body).get('body')
        print(class_info)
        name = class_info.get('classname')
        date_raw = class_info.get('date')
        print("date raw", date_raw)
        date = datetime.date(date_raw["year"], date_raw["month"], date_raw["day"])
        if not Class.objects.filter(name=name, date=date).exists():
            return HttpResponse("This time slot or class name does not exist!")
        class_to_remove = Class.objects.filter(name=name, date=date)
        class_to_remove.delete()
        return HttpResponse("Class Cancelled Successfully!")


@api_view(["POST"])
@csrf_exempt
def RemoveClasses(request):
    if request.method == "POST":
        if not request.user.is_superuser:
            return HttpResponse("Not Admin", status=403)
        class_info = json.loads(request.body).get('body')
        name = class_info.get('name')
        if not Classes.objects.filter(name=name).exists():
            return HttpResponse("No such class exists!")
        class_to_remove = Classes.objects.filter(name=name)
        class_to_remove.delete()
        return HttpResponse("Classes Cancelled Successfully!")


@api_view(["GET"])
@csrf_exempt
def ListClasses(request, id):
    if request.method == "GET":
        studio = Studio.objects.get(id=id)
        if studio is None:
            return HttpResponse("No studio found", status=404)
        now = datetime.datetime.now()
        order_class = Class.objects.filter(
            studio=studio).order_by('date', 'start_time')
        data = []
        for class_inst in order_class:
            print(class_inst.date, now.date(),
                  class_inst.start_time, now.time())
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
        if not request.user.is_authenticated:
            print("Did not login")
            return HttpResponse("Login in first to enroll a class!", status=403)
        studio = Studio.objects.get(id=id)
        if studio is None:
            print("no such studio")
            return HttpResponse("No studio found", status=404)
        data = json.loads(request.body).get("data")
        classes = Classes.objects.get(
            studio=studio, name=data.get("classname"))
        if classes.capacity == 0:
            return HttpResponse("Enrolling failed! The class is full!")
        else:
            # username = data.get("username")
            # user = User.objects.get(username=username)
            user = request.user
            # sub_user = StripeUser.objects.get(user_id=user)

            user_logs = StripeUserLog.objects.all().filter(user_id=request.user.id)

            stripe_customer_ids = []

            for log in user_logs:
                stripe_customer_ids.append(log.stripe_customer_id)

            try:
                sub = False
                for customer_id in stripe_customer_ids:
                    invoices = stripe.Invoice.list(customer=customer_id).data
                    for invoice in invoices:
                        curr_period_end = invoice.lines.data[0].period["end"]
                        curr_time = time.time()
                        if curr_period_end > curr_time:
                            sub = True
                            break
            except Exception as e:
                return JsonResponse({"error": str(e)})

            if sub is False:
                print("subscribe first")
                return HttpResponse("Need subscribe first to enroll the class!", status=403)
            else:
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
        # user = User.objects.get(username=info.get("username"))
        user = request.user
        if not user.is_authenticated:
            return HttpResponse("Login in first to quit a class!", status=403)
        info = json.loads(request.body)
        if user is None:
            return HttpResponse("No such user!", status=404)
        user_classes_lst = user.classes
        user_class_lst = user.class_lst
        classes = Classes.objects.get(name=info.get("classname"))
        user_classes_lst.remove(classes)
        class_lst = Class.objects.filter(name=info.get("classname"))
        for class_inst in class_lst:
            user_class_lst.remove(class_inst)

        new_cap = classes.capacity + 1
        classes.capacity = new_cap
        return HttpResponse("Class dropped successfully!")


@api_view(["POST"])
@csrf_exempt
def DeleteClass(request):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return HttpResponse("Login in first to delete a class!", status=403)
        info = json.loads(request.body)
        if user is None:
            return HttpResponse("No such user!", status=404)
        user_class_lst = user.class_lst
        date_raw = info.get("date")
        year = date_raw["year"]
        month = date_raw["month"]
        day = date_raw["day"]
        class_date = datetime.date(year, month, day)
        class_to_delete = Class.objects.get(
            name=info.get("classname"), date=class_date)
        if class_to_delete is None:
            return HttpResponse("No class session found!")
        user_class_lst.remove(class_to_delete)
        return HttpResponse("Class session delete successfully!")


@api_view(["GET"])
@csrf_exempt
def UserSchedule(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return HttpResponse("Login in first to view schedule!", status=403)
        # info = json.loads(request.body)
        # user = User.objects.get(username=info.get("username"))
        user = request.user
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


@api_view(["GET"])
@csrf_exempt
def SearchClass(request, id):
    if request.method == "GET":
        studio = Studio.objects.get(id=id)
        if studio is None:
            return HttpResponse("No studio found", status=404)
        search_key = json.loads(request.body)
        coach = search_key.get("coach")
        class_name = search_key.get("classname")

        class_lst = Class.objects.filter(studio=studio)
        if coach is not None:
            class_lst = class_lst.filter(coach=coach)

        if class_name is not None:
            class_lst = class_lst.filter(name=class_name)

        date_raw = search_key.get("date")
        if date_raw is not None:
            date = datetime.date(date_raw["year"], date_raw["month"], date_raw["day"])
            class_lst = class_lst.filter(date=date)

        data = []

        start_raw = search_key.get("start")
        end_raw = search_key.get("end")
        if start_raw is not None and end_raw is not None:
            start = datetime.time(start_raw["hour"], start_raw["minute"])
            end = datetime.time(end_raw["hour"], end_raw["minute"])
            for class_inst in class_lst:
                if class_inst.start_time > start and class_inst.end_time < end:
                    class_info = {"name": class_inst.name, "start_time": class_inst.start_time,
                                  "end_time": class_inst.end_time, "date": class_inst.date}
                    data.append(class_info)

        if start_raw is not None and end_raw is None:
            start = datetime.time(start_raw["hour"], start_raw["minute"])
            for class_inst in class_lst:
                if class_inst.start_time > start:
                    class_info = {"name": class_inst.name, "start_time": class_inst.start_time,
                                  "end_time": class_inst.end_time, "date": class_inst.date}
                    data.append(class_info)

        if start_raw is None and end_raw is not None:
            end = datetime.time(end_raw["hour"], end_raw["minute"])
            for class_inst in class_lst:
                if class_inst.end_time < end:
                    class_info = {"name": class_inst.name, "start_time": class_inst.start_time,
                                  "end_time": class_inst.end_time, "date": class_inst.date}
                    data.append(class_info)

        if start_raw is None and end_raw is None:
            for class_inst in class_lst:
                class_info = {"name": class_inst.name, "start_time": class_inst.start_time,
                              "end_time": class_inst.end_time, "date": class_inst.date}
                data.append(class_info)

        return JsonResponse(data, safe=False)

@api_view(["POST"])
@csrf_exempt
def SearchClasses(request, id):
    if request.method == "POST":
        studio = Studio.objects.get(id=id)
        if studio is None:
            return HttpResponse("No studio found", status=404)
        search_key = json.loads(request.body).get("body")
        print(search_key)
        coach = search_key.get("coach")
        class_name = search_key.get("classname")
        class_lst = Class.objects.filter(studio=studio)
        if coach is not None:
            class_lst = class_lst.filter(coach=coach)

        if class_name is not None:
            class_lst = class_lst.filter(name=class_name)

        date_raw = search_key.get("date")
        if date_raw is not None:
            date = datetime.date(date_raw["year"], date_raw["month"], date_raw["day"])
            print(date)
            class_lst = class_lst.filter(date=date)
            print(class_lst)

        data = []

        start_raw = search_key.get("start")
        end_raw = search_key.get("end")
        if start_raw is not None and end_raw is not None:
            start = datetime.time(start_raw["hour"], start_raw["minute"])
            end = datetime.time(end_raw["hour"], end_raw["minute"])
            for class_inst in class_lst:
                if class_inst.start_time > start and class_inst.end_time < end:
                    class_info = {"name": class_inst.name, "start_time": class_inst.start_time,
                                  "end_time": class_inst.end_time, "date": class_inst.date}
                    data.append(class_info)

        if start_raw is not None and end_raw is None:
            start = datetime.time(start_raw["hour"], start_raw["minute"])
            for class_inst in class_lst:
                if class_inst.start_time > start:
                    class_info = {"name": class_inst.name, "start_time": class_inst.start_time,
                                  "end_time": class_inst.end_time, "date": class_inst.date}
                    data.append(class_info)

        if start_raw is None and end_raw is not None:
            end = datetime.time(end_raw["hour"], end_raw["minute"])
            for class_inst in class_lst:
                if class_inst.end_time < end:
                    class_info = {"name": class_inst.name, "start_time": class_inst.start_time,
                                  "end_time": class_inst.end_time, "date": class_inst.date}
                    data.append(class_info)

        if start_raw is None and end_raw is None:
            for class_inst in class_lst:
                class_info = {"name": class_inst.name, "start_time": class_inst.start_time,
                              "end_time": class_inst.end_time, "date": class_inst.date}
                data.append(class_info)

        if data is None:
            return JsonResponse(data, safe=False)
        else:
            classes = dict()
            for class_inst in data:
                classes[class_inst["name"]] = {"start_time": class_inst["start_time"],
                                               "end_time": class_inst["end_time"]}

            classes_data = []
            for key in classes.keys():
                curr = Classes.objects.get(name=key)

                keyword_lst = []
                for keyword in curr.keywords.all():
                    keyword_lst.append(keyword.keyword)
                classes_info = {"classname": key, "description": curr.description, "coach": curr.coach,
                           "weekday": curr.weekday, "keywords": keyword_lst,
                           "start": classes.get(key)["start_time"], "end": classes.get(key)["end_time"]}
                classes_data.append(classes_info)

            return JsonResponse(classes_data, safe=False)

