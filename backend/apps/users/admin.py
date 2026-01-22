"""
Admin configuration for Users app.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Achievement, UserAchievement


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin for custom User model."""
    
    list_display = ['username', 'email', 'level', 'xp_points', 'streak_days', 'is_staff']
    list_filter = ['level', 'is_staff', 'is_active']
    search_fields = ['username', 'email']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Gamification', {
            'fields': ('xp_points', 'level', 'streak_days', 'last_activity_date')
        }),
        ('Trading', {
            'fields': ('virtual_balance',)
        }),
        ('Profile', {
            'fields': ('avatar', 'bio')
        }),
    )


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    """Admin for Achievement model."""
    
    list_display = ['name', 'category', 'xp_reward', 'condition_type', 'condition_value']
    list_filter = ['category']
    search_fields = ['name', 'description']


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    """Admin for UserAchievement model."""
    
    list_display = ['user', 'achievement', 'unlocked_at']
    list_filter = ['achievement__category']
    search_fields = ['user__username', 'achievement__name']
