from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from .models import Users
from .serializers import RegisterSerializer
import json


class RegistrationAPIView(CreateAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    queryset = Users.objects.all()

##retriveupdateapiview

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

