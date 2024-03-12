from django.urls import path

from community.views import post_list_create

urlpatterns = [
    path('posts/<int:search_id>', post_list_create, name='post_list_create')
]