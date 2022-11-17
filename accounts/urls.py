from django.contrib import admin
from django.urls import path
from django.urls import include  # ADDITION
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import RegistrationAPIView

# from accounts.views import CreateUsers
app_name = 'accounts'

urlpatterns = [
    # path("admin/", admin.site.urls),
    # path("accounts/", include("django.contrib.auth.urls")),  # ADDITION: include the default auth urls
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signup/', RegistrationAPIView.as_view(), name='registration_api_view')
    # path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    # path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh')
    # path('register/', Register_Users, name='auth_register'),
    # path('createusers/', CreateUsers)
]