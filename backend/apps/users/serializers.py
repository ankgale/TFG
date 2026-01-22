"""
Serializers for User app.
"""

from rest_framework import serializers
from .models import User, Achievement, UserAchievement


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    xp_to_next_level = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'avatar', 'bio',
            'xp_points', 'level', 'streak_days', 'xp_to_next_level',
            'virtual_balance', 'last_activity_date',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'xp_points', 'level', 'created_at', 'updated_at']


class AchievementSerializer(serializers.ModelSerializer):
    """Serializer for Achievement model."""
    
    class Meta:
        model = Achievement
        fields = [
            'id', 'name', 'description', 'icon', 'category',
            'xp_reward', 'condition_type', 'condition_value'
        ]


class UserAchievementSerializer(serializers.ModelSerializer):
    """Serializer for UserAchievement model."""
    
    achievement = AchievementSerializer(read_only=True)
    
    class Meta:
        model = UserAchievement
        fields = ['id', 'achievement', 'unlocked_at']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)