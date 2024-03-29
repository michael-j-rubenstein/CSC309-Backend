from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from .models import Users
from .serializers import SignupSerializer, ProfileSerializer, MePageSerializer


class RegistrationAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer

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


class UserProfileAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MePageSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            return Response(serializer.data)
