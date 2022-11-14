from django.shortcuts import render
from django.http import Http404


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404, RetrieveAPIView, ListAPIView

from .models import Studio
from .serializers import StudioSerializer
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

def AllStudios(request):
    if request.method == 'POST':
        print('asda')
