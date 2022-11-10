from django.urls import path, include

from .views import temp

urlpatterns = [
    path('test/', temp)
]