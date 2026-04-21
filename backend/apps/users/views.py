"""
API views for User app.
"""

from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Achievement, User, UserAchievement
from .serializers import (
    AchievementSerializer,
    RegisterSerializer,
    UserAchievementSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User model.
    Provides CRUD operations and user-specific actions.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=["get"])
    def progress(self, request, pk=None):
        """Get user's learning progress summary."""
        user = self.get_object()

        return Response(
            {
                "user_id": user.id,
                "level": user.level,
                "xp_points": user.xp_points,
                "xp_to_next_level": user.xp_to_next_level,
                "streak_days": user.streak_days,
                "virtual_balance": str(user.virtual_balance),
                "achievements_count": user.achievements.count(),
            }
        )

    @action(detail=True, methods=["post"])
    def add_xp(self, request, pk=None):
        """Add XP points to user."""
        user = self.get_object()
        amount = request.data.get("amount", 0)

        if amount <= 0:
            return Response(
                {"error": "Amount must be positive"}, status=status.HTTP_400_BAD_REQUEST
            )

        old_level = user.level
        user.add_xp(amount)

        return Response(
            {
                "xp_points": user.xp_points,
                "level": user.level,
                "leveled_up": user.level > old_level,
                "xp_to_next_level": user.xp_to_next_level,
            }
        )


class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Achievement model.
    Read-only as achievements are predefined.
    """

    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer


class UserAchievementViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for UserAchievement model.
    Shows achievements unlocked by the authenticated user.
    """

    serializer_class = UserAchievementSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = UserAchievement.objects.select_related("achievement", "user")
        if user.is_authenticated:
            return queryset.filter(user=user)
        return queryset.none()


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created"}, status=201)
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "user_id": user.id})
        return Response({"error": "Invalid credentials"}, status=401)


class LogoutView(APIView):
    """Delete the user's auth token server-side."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Logged out"})


class ChangePasswordView(APIView):
    """Allow authenticated users to change their password."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        current = request.data.get("current_password", "")
        new_pw = request.data.get("new_password", "")

        if not request.user.check_password(current):
            return Response(
                {"error": "La contraseña actual es incorrecta"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(new_pw) < 8:
            return Response(
                {"error": "La nueva contraseña debe tener al menos 8 caracteres"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.set_password(new_pw)
        request.user.save()
        request.user.auth_token.delete()
        token = Token.objects.create(user=request.user)
        return Response({"message": "Contraseña actualizada", "token": token.key})


class UpdateProfileView(APIView):
    """Allow authenticated users to update their profile (bio, email, avatar)."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        allowed = {"bio", "email", "avatar"}
        data = {k: v for k, v in request.data.items() if k in allowed}
        serializer = UserSerializer(request.user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeaderboardView(APIView):
    """Public leaderboard — top users by XP."""

    def get(self, request):
        top_users = User.objects.order_by("-xp_points", "-level")[:20]
        data = [
            {
                "rank": idx + 1,
                "username": u.username,
                "level": u.level,
                "xp_points": u.xp_points,
                "streak_days": u.streak_days,
                "avatar": u.avatar,
            }
            for idx, u in enumerate(top_users)
            if not u.is_staff
        ]
        return Response(data)


class DailyChallengeView(APIView):
    """Return today's daily-challenge progress for the authenticated user."""

    DAILY_GOAL = 3

    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"completed_today": 0, "goal": self.DAILY_GOAL})

        from apps.lessons.models import UserLessonProgress

        today = timezone.localdate()
        completed_today = UserLessonProgress.objects.filter(
            user=user,
            status="completed",
            completed_at__date=today,
        ).count()

        return Response(
            {
                "completed_today": completed_today,
                "goal": self.DAILY_GOAL,
            }
        )
