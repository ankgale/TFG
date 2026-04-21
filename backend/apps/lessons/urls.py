"""
URL configuration for Lessons app.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import LessonViewSet, ModuleViewSet, QuizViewSet, UserProgressViewSet

router = DefaultRouter()
router.register(r"modules", ModuleViewSet, basename="module")
router.register(r"lessons", LessonViewSet, basename="lesson")
router.register(r"quizzes", QuizViewSet, basename="quiz")
router.register(r"progress", UserProgressViewSet, basename="progress")

urlpatterns = [
    path("", include(router.urls)),
]
