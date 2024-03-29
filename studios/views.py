from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError

from .models import Studio, AmmenitySet, ImageSet
from classes.models import Classes, Class

import json
import math

# Create your views here.


@api_view(['POST'])
@permission_classes([AllowAny])
def AllStudios(request):

    if request.method == 'POST':
        payload = json.loads(request.body)

        user_lat = payload.get("latitude", '')
        user_long = payload.get("longitude", '')

        if user_lat == '' or user_long == '':
            raise ValidationError

        studio_queryset = Studio.objects.all()

        filter_name = payload.get("name", '')
        filter_amenities = payload.get("amenities", '')
        filter_classes = payload.get("classes", '')
        filter_coaches = payload.get("coaches", '')

        response = {}

        studios = []

        for s in studio_queryset:

            # check filtering conditions
            name_satisfied = False if filter_name != '' else True
            amenities_satisfied = False if filter_amenities != '' else True
            classes_satisfied = False if filter_classes != '' else True
            coaches_satisfied = False if filter_coaches != '' else True

            if not name_satisfied and s.name == filter_name:
                name_satisfied = True

            if not amenities_satisfied:
                all_amenities = s.ammenities.all()
                satisfied = True
                for ammenity in filter_amenities:
                    if len(all_amenities.filter(type=ammenity)) == 0:
                        satisfied = False
                        break
                amenities_satisfied = True if satisfied else False

            if not classes_satisfied:
                studio_classes = Classes.objects.all().filter(studio=s.id)
                satisfied = True
                for wanted_class in filter_classes:
                    if len(studio_classes.filter(name=wanted_class)) == 0:
                        satisfied = False
                        break
                classes_satisfied = True if satisfied else False

            if not coaches_satisfied:
                studio_classes = Classes.objects.all().filter(studio=s.id)
                satisfied = True
                for wanted_coach in filter_coaches:
                    if len(studio_classes.filter(coach=wanted_coach)) == 0:
                        satisfied = False
                coaches_satisfied = True if satisfied else False

            all_conditions_satisfied = name_satisfied and amenities_satisfied and classes_satisfied and coaches_satisfied

            # if exists one condition not satisfied, then continue to next studio
            if not all_conditions_satisfied:
                continue

            studio = s.__dict__
            studio.pop('_state')

            # get the destination part of the url
            url_dest = studio['address'].replace(
                ' ', '+') + '+' + studio['postal'].replace('', '+')

            # get the actual google maps directions url
            url = "http://maps.google.com/maps/dir/" + \
                str(user_lat) + ",+" + str(user_long) + "/" + url_dest

            # difference in latitude and longitude converted to KM (apporximation)
            lat_diff = abs(studio['latitude'] - user_lat) * 111.1
            long_diff = abs(studio['longitude'] - user_long) * 111.1

            # get approx straight line distance
            distance = math.sqrt(lat_diff ** 2 + long_diff ** 2)
            studio['distance'] = round(distance, 2)

            # remove / add some data
            studio.pop('phone_num')
            studio.pop('postal')
            studio['directions'] = url

            studios.append(studio)

        # sort studios in ascending order via the distance to current location
        studios = sorted(studios, key=lambda d: d['distance'])

        # populate response dictionary
        for s in studios:
            response[s['name']] = s

        return JsonResponse(response)


@api_view(['GET'])
@permission_classes([AllowAny])
def StudioInformation(request, id):
    if request.method == 'GET':
        studio = get_object_or_404(Studio, id=id)
        # studio = studio.__dict__
        # studio.pop('_state')
        name, address, lat, long, postal, phone = studio.name,\
            studio.address, studio.latitude,\
            studio.latitude, studio.postal, studio.phone_num
        classes_raw = Classes.objects.filter(studio=studio)

        class_lst = []
        if classes_raw is not None:
            for classes in classes_raw.all():
                capacity = classes.capacity
                if capacity == 0:
                    continue
                class_name, description, coach, weekday = classes.name, classes.description, classes.coach, classes.weekday
                keywords_lst = [
                    keyword.keyword for keyword in classes.keywords.all()]
                class_inst = Class.objects.filter(classes=classes).all()[0]
                start_time = class_inst.start_time
                end_time = class_inst.end_time
                class_data = {"classname": class_name, "description": description, "coach": coach, "weekday": weekday,
                              "keywords": keywords_lst, "start": start_time, "end": end_time}
                class_lst.append(class_data)
        amenities_lst = []
        images_lst = []
        images = ImageSet.objects.filter(studio=studio)
        amenities = AmmenitySet.objects.filter(studio=studio)

        url_dest = address.replace(
            ' ', '+') + '+' + postal.replace('', '+')

        if amenities is not None:
            amenities_lst = [{"name": amenity.type.type, "quantity": amenity.quanitity}
                             for amenity in amenities.all()]
        if images is not None:
            images_lst = [image.image.image.url for image in images]
        data = {"name": name, "address": address, "latitude": lat, "longitude": long, "postal": postal, "phone": phone,
                "phone_num": phone, "amenities": amenities_lst, "images": images_lst, "classes": class_lst, "url_dest": url_dest}
        print(data)
        return JsonResponse(data, safe=False)
