from django.urls import path
from .views import *
from django.urls import path

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('userslist/', UsersListAPIView.as_view(), name='users_list_api'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('verify-token/', TokenVerificationView.as_view(), name='verify_token'),
]
