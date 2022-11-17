from django.urls import path, include
from .views import AllStudios, StudioInformation

urlpatterns = [
    path('', AllStudios, name='all studios'),
    path('<int:id>/', StudioInformation, name='studio information')
]
