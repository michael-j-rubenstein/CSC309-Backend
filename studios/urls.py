from django.urls import path, include
from .views import AllStudios

urlpatterns = [
    path('all/',
         AllStudios, name='all')
]
