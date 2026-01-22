"""
URL configuration for Users app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, AchievementViewSet, UserAchievementViewSet, RegisterView, LoginView

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')
router.register(r'achievements', AchievementViewSet, basename='achievement')
router.register(r'user-achievements', UserAchievementViewSet, basename='user-achievement')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]
