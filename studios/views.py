from django.shortcuts import render
from django.http import Http404, JsonResponse

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404, RetrieveAPIView, ListAPIView
from rest_framework.exceptions import ValidationError

from .models import Studio
from .serializers import StudioSerializer

import json
import math
import requests

# Create your views here.


# class TestView(APIView):
#     def get(self, request, *args, **kwargs):
#         a = False
#         return Response({
#             "test data": "adsada",
#             "aaaa": "bbbbb",
#             "asda": 1 if a else None
#         })

# need to define serializers to use crud views
# class TestView(RetrieveAPIView):
#     serializer_class = StudioSerializer

#     def get_object(self):
#         if self.kwargs['lat_positive'] not in {'t', 'f'} or self.kwargs['long_positive'] not in {'t', 'f'}:
#             raise Http404

#         lat_is_positive = True if self.kwargs['lat_positive'] == 't' else False
#         long_is_positive = True if self.kwargs['long_positive'] == 't' else False

#         user_lat = self.kwargs['lat'] if lat_is_positive else - \
#             self.kwargs['lat']
#         user_long = self.kwargs['long'] if long_is_positive else - \
#             self.kwargs['long']

#         all_studios_queryset = Studio.objects.all()

#         for studio in all_studios_queryset:
#             print(studio.name)

#         return get_object_or_404(Studio, id=1)

# @api_view(['GET', 'POST'])
@api_view(['POST'])
def AllStudios(request):

    # if request.method == 'GET':
    #     return JsonResponse({'message': "Post location data to get nearby studios"})

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
