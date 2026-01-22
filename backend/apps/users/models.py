"""
User models for FinLearn.
Custom user model with gamification fields.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model with gamification and progress tracking.
    Extends Django's AbstractUser for future auth implementation.
    """
    
    # Profile
    avatar = models.URLField(blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    
    # Gamification
    xp_points = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    streak_days = models.PositiveIntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)
    
    # Virtual money for stock simulation
    virtual_balance = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=100000.00  # Start with $100,000 virtual money
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.username
    
    def add_xp(self, amount: int) -> None:
        """Add XP points and check for level up."""
        self.xp_points += amount
        # Level up every 1000 XP
        new_level = (self.xp_points // 1000) + 1
        if new_level > self.level:
            self.level = new_level
        self.save()
    
    @property
    def xp_to_next_level(self) -> int:
        """Calculate XP needed for next level."""
        return (self.level * 1000) - self.xp_points


class Achievement(models.Model):
    """
    Achievements that users can unlock.
    """
    
    CATEGORY_CHOICES = [
        ('learning', 'Learning'),
        ('trading', 'Trading'),
        ('streak', 'Streak'),
        ('special', 'Special'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)  # Icon name/class
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    xp_reward = models.PositiveIntegerField(default=100)
    
    # Unlock conditions (stored as JSON-like structure)
    condition_type = models.CharField(max_length=50)  # e.g., 'lessons_completed', 'streak_days'
    condition_value = models.PositiveIntegerField()  # e.g., 10 lessons, 7 days
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'achievements'
    
    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    """
    Track which achievements each user has unlocked.
    """
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='achievements',
        null=True,  # Nullable for now (no auth yet)
        blank=True
    )
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_achievements'
        unique_together = ['user', 'achievement']
    
    def __str__(self):
        return f"{self.user} - {self.achievement}"
