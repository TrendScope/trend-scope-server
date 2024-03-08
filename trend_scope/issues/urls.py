from django.urls import path

from issues.views import get_histories

urlpatterns = [
    path('histories', get_histories, name='get_histories')
]