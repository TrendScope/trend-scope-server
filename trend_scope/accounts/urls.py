from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import check_duplicate_id

urlpatterns = [
    path('registration', include('dj_rest_auth.registration.urls')),
    path('registration/id-check', check_duplicate_id, name='check_duplicate_id'),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]