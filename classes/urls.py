from django.urls import path, include
from classes.views import CreateClasses, ListClasses, RemoveClass, RemoveClasses, EnrollClasses

app_name = 'classes'

urlpatterns = [
    # path('<int:id>/classlist/', ListClassView, name="list_classes"),
    path('<int:id>/createclass/', CreateClasses, name="create_classes"),
    path('<int:id>/classes/', ListClasses, name="list_classes"),
    path('removeclass/', RemoveClass, name="remove_class"),
    path('removeclasses/', RemoveClasses, name="remove_classes"),
    path('<int:id>/enrollclass', EnrollClasses, name="enroall_classes"),
]