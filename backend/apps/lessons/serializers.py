"""
Serializers for Lessons app.
"""

from rest_framework import serializers
from .models import Module, Lesson, Quiz, QuizOption, UserLessonProgress, UserModuleProgress


class QuizOptionSerializer(serializers.ModelSerializer):
    """Serializer for QuizOption model."""
    
    class Meta:
        model = QuizOption
        fields = ['id', 'text', 'is_correct', 'order']


class QuizSerializer(serializers.ModelSerializer):
    """Serializer for Quiz model."""
    
    options = QuizOptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Quiz
        fields = [
            'id', 'question', 'question_type', 'explanation',
            'order', 'xp_reward', 'options'
        ]


class LessonSerializer(serializers.ModelSerializer):
    """Serializer for Lesson model."""
    
    quizzes = QuizSerializer(many=True, read_only=True)
    quizzes_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Lesson
        fields = [
            'id', 'module', 'title', 'description', 'content',
            'order', 'xp_reward', 'estimated_time',
            'is_published', 'quizzes', 'quizzes_count'
        ]
    
    def get_quizzes_count(self, obj):
        return obj.quizzes.count()


class LessonListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for lesson lists."""
    
    quizzes_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Lesson
        fields = [
            'id', 'title', 'description', 'order',
            'xp_reward', 'estimated_time', 'quizzes_count'
        ]
    
    def get_quizzes_count(self, obj):
        return obj.quizzes.count()


class ModuleSerializer(serializers.ModelSerializer):
    """Serializer for Module model."""
    
    lessons = LessonListSerializer(many=True, read_only=True)
    lessons_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Module
        fields = [
            'id', 'title', 'description', 'icon', 'color',
            'difficulty', 'order', 'xp_reward',
            'is_published', 'lessons', 'lessons_count',
            'created_at', 'updated_at'
        ]


class ModuleListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for module lists."""
    
    lessons_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Module
        fields = [
            'id', 'title', 'description', 'icon', 'color',
            'difficulty', 'order', 'xp_reward', 'lessons_count'
        ]


class UserLessonProgressSerializer(serializers.ModelSerializer):
    """Serializer for UserLessonProgress model."""
    
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)
    
    class Meta:
        model = UserLessonProgress
        fields = [
            'id', 'user', 'lesson', 'lesson_title',
            'status', 'score', 'attempts',
            'started_at', 'completed_at'
        ]
        read_only_fields = ['user']


class UserModuleProgressSerializer(serializers.ModelSerializer):
    """Serializer for UserModuleProgress model."""
    
    module_title = serializers.CharField(source='module.title', read_only=True)
    progress_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = UserModuleProgress
        fields = [
            'id', 'user', 'module', 'module_title',
            'lessons_completed', 'is_completed', 'progress_percentage',
            'started_at', 'completed_at'
        ]
        read_only_fields = ['user']
