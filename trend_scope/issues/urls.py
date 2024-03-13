from django.urls import path

from issues.views import get_histories, get_categories

urlpatterns = [
    path('categories', get_categories, name='get_categories'),
    path('histories', get_histories, name='get_histories')
]