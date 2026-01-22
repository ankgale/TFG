"""
API views for User app.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from .models import User, Achievement, UserAchievement
from .serializers import UserSerializer, AchievementSerializer, UserAchievementSerializer, RegisterSerializer, LoginSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User model.
    Provides CRUD operations and user-specific actions.
    """
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=True, methods=['get'])
    def progress(self, request, pk=None):
        """Get user's learning progress summary."""
        user = self.get_object()
        
        # This will be expanded when lessons app is integrated
        return Response({
            'user_id': user.id,
            'level': user.level,
            'xp_points': user.xp_points,
            'xp_to_next_level': user.xp_to_next_level,
            'streak_days': user.streak_days,
            'virtual_balance': str(user.virtual_balance),
            'achievements_count': user.achievements.count(),
        })
    
    @action(detail=True, methods=['post'])
    def add_xp(self, request, pk=None):
        """Add XP points to user."""
        user = self.get_object()
        amount = request.data.get('amount', 0)
        
        if amount <= 0:
            return Response(
                {'error': 'Amount must be positive'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        old_level = user.level
        user.add_xp(amount)
        
        return Response({
            'xp_points': user.xp_points,
            'level': user.level,
            'leveled_up': user.level > old_level,
            'xp_to_next_level': user.xp_to_next_level,
        })


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
    Shows achievements unlocked by users.
    """
    
    queryset = UserAchievement.objects.select_related('achievement', 'user')
    serializer_class = UserAchievementSerializer
    
    def get_queryset(self):
        """Filter by user_id if provided."""
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        return queryset


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User created'}, status=201)
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user_id': user.id})
        return Response({'error': 'Invalid credentials'}, status=401)