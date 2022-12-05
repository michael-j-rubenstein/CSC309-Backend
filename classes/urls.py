from django.urls import path, include
from classes.views import CreateClasses, ListClasses, RemoveClass, RemoveClasses, EnrollClasses, DeleteClass, DeleteClasses, UserSchedule, SearchClass, EditClasses

app_name = 'classes'

urlpatterns = [
    # path('<int:id>/classlist/', ListClassView, name="list_classes"),
    path('<int:id>/createclass/', CreateClasses, name="create_classes"),
    path('<int:id>/classes/', ListClasses, name="list_classes"),
    path('removeclass/', RemoveClass, name="remove_class"),
    path('removeclasses/', RemoveClasses, name="remove_classes"),
    path('<int:id>/enrollclass/', EnrollClasses, name="enroll_classes"),
    path('deleteclasses/', DeleteClasses, name="delete_classes"),
    path('deleteclass/', DeleteClass, name="delete_class"),
    path('schedule/', UserSchedule, name="user_schedule"),
    path('<int:id>/searchclass/', SearchClass, name="search_class"),
    path('<int:id>/editclasses/', EditClasses, name="edit_classes")
]