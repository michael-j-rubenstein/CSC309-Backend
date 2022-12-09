from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.views import RegistrationAPIView, UserUpdateAPIView, UserProfileAPIView

app_name = 'accounts'

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signup/', RegistrationAPIView.as_view(), name='registration_api_view'),
    path('edit/', UserUpdateAPIView.as_view(), name='user_update_api_view'),
    path('me/', UserProfileAPIView.as_view(), name='user_profile_api_view')
]