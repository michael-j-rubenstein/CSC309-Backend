from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError

from .models import Studio

import json
import math

# Create your views here.


@api_view(['POST'])
def AllStudios(request):

    if request.method == 'POST':
        payload = json.loads(request.body)

        user_lat = payload.get("latitude", '')
        user_long = payload.get("longitude", '')

        if user_lat == '' or user_long == '':
            raise ValidationError

        studio_queryset = Studio.objects.all()

        response = {}

        studios = []

        for s in studio_queryset:
            studio = s.__dict__
            studio.pop('_state')

            url_dest = studio['address'].replace(
                ' ', '+') + '+' + studio['postal'].replace('', '+')

            url = "http://maps.google.com/maps/dir/" + \
                str(user_lat) + ",+" + str(user_long) + "/" + url_dest

            lat_diff = abs(studio['latitude'] - user_lat) * \
                111.1           # converted to KM
            long_diff = abs(studio['longitude'] -
                            user_long) * 111.1  # converted to KM
            distance = math.sqrt(lat_diff ** 2 + long_diff ** 2)
            studio['distance'] = round(distance, 2)
            studios.append(studio)
            studio.pop('latitude')
            studio.pop('longitude')
            studio.pop('phone_num')
            studio.pop('postal')
            studio['directions'] = url

        studios = sorted(studios, key=lambda d: d['distance'])

        for s in studios:
            response[s['name']] = s

        return JsonResponse(response)


@api_view(['GET'])
def StudioInformation(request, id):
    if request.method == 'GET':
        studio = get_object_or_404(Studio, id=id)
        studio = studio.__dict__
        studio.pop('_state')
        return JsonResponse(studio)
