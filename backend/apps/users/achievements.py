"""
Achievement checking logic.
Called after lesson completions and trades to award newly unlocked achievements.
"""

from apps.lessons.models import UserLessonProgress, UserModuleProgress
from apps.stocks.models import Transaction

from .models import Achievement, UserAchievement

CONDITION_CHECKERS = {
    "lessons_completed": lambda user: UserLessonProgress.objects.filter(
        user=user, status="completed"
    ).count(),
    "modules_completed": lambda user: UserModuleProgress.objects.filter(
        user=user, is_completed=True
    ).count(),
    "streak_days": lambda user: user.streak_days,
    "xp_points": lambda user: user.xp_points,
    "trades_executed": lambda user: Transaction.objects.filter(user=user).count(),
    "level_reached": lambda user: user.level,
}


def check_achievements(user):
    """
    Evaluate all achievements the user hasn't unlocked yet.
    Returns a list of newly unlocked Achievement objects.
    """
    if not user or not user.is_authenticated:
        return []

    already_unlocked = set(
        UserAchievement.objects.filter(user=user).values_list(
            "achievement_id", flat=True
        )
    )

    new_achievements = []

    for achievement in Achievement.objects.all():
        if achievement.id in already_unlocked:
            continue

        checker = CONDITION_CHECKERS.get(achievement.condition_type)
        if not checker:
            continue

        current_value = checker(user)
        if current_value >= achievement.condition_value:
            UserAchievement.objects.create(user=user, achievement=achievement)
            user.add_xp(achievement.xp_reward)
            new_achievements.append(achievement)

    return new_achievements
