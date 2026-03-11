"""
URL configuration for Users app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet, AchievementViewSet, UserAchievementViewSet,
    RegisterView, LoginView, LogoutView,
    ChangePasswordView, UpdateProfileView,
    LeaderboardView, DailyChallengeView,
)

router = DefaultRouter()
router.register(r'profiles', UserViewSet, basename='user')
router.register(r'achievements', AchievementViewSet, basename='achievement')
router.register(r'user-achievements', UserAchievementViewSet, basename='user-achievement')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('profile/', UpdateProfileView.as_view(), name='profile'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('daily-challenge/', DailyChallengeView.as_view(), name='daily-challenge'),
    path('', include(router.urls)),
]
