"""
URL configuration for FinLearn project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/users/', include('apps.users.urls')),
    path('api/lessons/', include('apps.lessons.urls')),
    path('api/stocks/', include('apps.stocks.urls')),
]
