from django.contrib import admin
from django.urls import path, include

from issues.views import get_categories

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('accounts.urls')),
    path('api/v1/issues/', include('issues.urls')),
    path('api/v1/community/', include('community.urls')),
]
