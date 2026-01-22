"""
Admin configuration for Lessons app.
"""

from django.contrib import admin
from .models import Module, Lesson, Quiz, QuizOption, UserLessonProgress, UserModuleProgress


class LessonInline(admin.TabularInline):
    """Inline for lessons in module admin."""
    model = Lesson
    extra = 1
    fields = ['title', 'order', 'xp_reward', 'estimated_time', 'is_published']


class QuizOptionInline(admin.TabularInline):
    """Inline for quiz options in quiz admin."""
    model = QuizOption
    extra = 4
    fields = ['text', 'is_correct', 'order']


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    """Admin for Module model."""
    
    list_display = ['title', 'difficulty', 'order', 'lessons_count', 'xp_reward', 'is_published']
    list_filter = ['difficulty', 'is_published']
    search_fields = ['title', 'description']
    ordering = ['order']
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Admin for Lesson model."""
    
    list_display = ['title', 'module', 'order', 'xp_reward', 'estimated_time', 'is_published']
    list_filter = ['module', 'is_published']
    search_fields = ['title', 'content']
    ordering = ['module', 'order']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Admin for Quiz model."""
    
    list_display = ['question_preview', 'lesson', 'question_type', 'xp_reward']
    list_filter = ['question_type', 'lesson__module']
    search_fields = ['question']
    inlines = [QuizOptionInline]
    
    def question_preview(self, obj):
        return obj.question[:50] + '...' if len(obj.question) > 50 else obj.question
    question_preview.short_description = 'Question'


@admin.register(UserLessonProgress)
class UserLessonProgressAdmin(admin.ModelAdmin):
    """Admin for UserLessonProgress model."""
    
    list_display = ['user', 'lesson', 'status', 'score', 'attempts']
    list_filter = ['status', 'lesson__module']
    search_fields = ['user__username', 'lesson__title']


@admin.register(UserModuleProgress)
class UserModuleProgressAdmin(admin.ModelAdmin):
    """Admin for UserModuleProgress model."""
    
    list_display = ['user', 'module', 'lessons_completed', 'is_completed']
    list_filter = ['is_completed', 'module']
    search_fields = ['user__username', 'module__title']
