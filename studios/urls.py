from django.urls import path, include
from .views import AllStudios, StudioInformation

urlpatterns = [
    path('all/', AllStudios, name='all'),
    path('<int:id>/', StudioInformation, name='studio')
]
