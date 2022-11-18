from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView

from .models import Users
from .serializers import RegisterSerializer, ProfileSerializer
import json


class RegistrationAPIView(CreateAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    queryset = Users.objects.all()


class UserUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def update(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    # def get_object(self):
    #     # authentication class assigns user to request
    #     return self.request.user
    #
    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)
#retriveupdateapiview

# def post(self, request):
#
#     user = request.data.get('users', {})
#     serializer = self.serializer_class(data=user)
#     # print(serializer)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data, status=status.HTTP_201_CREATED)

# def get(self, request):
#     Users = self.get_queryset()
#     return Response(Users)
