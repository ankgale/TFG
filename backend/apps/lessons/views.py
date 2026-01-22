"""
API views for Lessons app.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from .models import Module, Lesson, Quiz, UserLessonProgress, UserModuleProgress
from .serializers import (
    ModuleSerializer, ModuleListSerializer,
    LessonSerializer, LessonListSerializer,
    QuizSerializer,
    UserLessonProgressSerializer, UserModuleProgressSerializer
)


class ModuleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Module model.
    Provides CRUD operations for learning modules.
    """
    
    queryset = Module.objects.filter(is_published=True).prefetch_related('lessons')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ModuleListSerializer
        return ModuleSerializer
    
    @action(detail=True, methods=['get'])
    def lessons(self, request, pk=None):
        """Get all lessons for a module."""
        module = self.get_object()
        lessons = module.lessons.filter(is_published=True)
        serializer = LessonListSerializer(lessons, many=True)
        return Response(serializer.data)


class LessonViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Lesson model.
    Provides CRUD operations for lessons.
    """
    
    queryset = Lesson.objects.filter(is_published=True).select_related('module')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return LessonListSerializer
        return LessonSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        module_id = self.request.query_params.get('module_id')
        
        if module_id:
            queryset = queryset.filter(module_id=module_id)
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def quizzes(self, request, pk=None):
        """Get all quizzes for a lesson."""
        lesson = self.get_object()
        quizzes = lesson.quizzes.prefetch_related('options')
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """Mark a lesson as started."""
        lesson = self.get_object()
        user_id = request.data.get('user_id')  # Temporary until auth
        
        progress, created = UserLessonProgress.objects.get_or_create(
            user_id=user_id,
            lesson=lesson,
            defaults={
                'status': 'in_progress',
                'started_at': timezone.now()
            }
        )
        
        if not created and progress.status == 'not_started':
            progress.status = 'in_progress'
            progress.started_at = timezone.now()
            progress.save()
        
        serializer = UserLessonProgressSerializer(progress)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark a lesson as completed."""
        lesson = self.get_object()
        user_id = request.data.get('user_id')  # Temporary until auth
        score = request.data.get('score', 100)
        
        progress, created = UserLessonProgress.objects.get_or_create(
            user_id=user_id,
            lesson=lesson,
            defaults={
                'status': 'completed',
                'score': score,
                'attempts': 1,
                'started_at': timezone.now(),
                'completed_at': timezone.now()
            }
        )
        
        if not created:
            progress.status = 'completed'
            progress.score = max(progress.score, score)
            progress.attempts += 1
            progress.completed_at = timezone.now()
            progress.save()
        
        # Update module progress
        self._update_module_progress(user_id, lesson.module)
        
        serializer = UserLessonProgressSerializer(progress)
        return Response({
            'progress': serializer.data,
            'xp_earned': lesson.xp_reward if created else 0
        })
    
    def _update_module_progress(self, user_id, module):
        """Update module progress when a lesson is completed."""
        if not user_id:
            return
        
        completed_lessons = UserLessonProgress.objects.filter(
            user_id=user_id,
            lesson__module=module,
            status='completed'
        ).count()
        
        total_lessons = module.lessons_count
        
        module_progress, _ = UserModuleProgress.objects.get_or_create(
            user_id=user_id,
            module=module,
            defaults={'started_at': timezone.now()}
        )
        
        module_progress.lessons_completed = completed_lessons
        
        if completed_lessons >= total_lessons:
            module_progress.is_completed = True
            module_progress.completed_at = timezone.now()
        
        module_progress.save()


class QuizViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Quiz model.
    Read-only as quizzes are managed through admin.
    """
    
    queryset = Quiz.objects.prefetch_related('options')
    serializer_class = QuizSerializer
    
    @action(detail=True, methods=['post'])
    def answer(self, request, pk=None):
        """Check if the provided answer is correct."""
        quiz = self.get_object()
        option_id = request.data.get('option_id')
        
        try:
            option = quiz.options.get(id=option_id)
            is_correct = option.is_correct
            
            return Response({
                'is_correct': is_correct,
                'correct_answer': quiz.options.filter(is_correct=True).first().text,
                'explanation': quiz.explanation,
                'xp_earned': quiz.xp_reward if is_correct else 0
            })
        except Exception:
            return Response(
                {'error': 'Invalid option'},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserProgressViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing user progress.
    """
    
    serializer_class = UserModuleProgressSerializer
    
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        queryset = UserModuleProgress.objects.select_related('module')
        
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get overall progress summary."""
        user_id = request.query_params.get('user_id')
        
        if not user_id:
            return Response({
                'total_modules': Module.objects.filter(is_published=True).count(),
                'total_lessons': Lesson.objects.filter(is_published=True).count(),
                'completed_modules': 0,
                'completed_lessons': 0,
                'total_xp_earned': 0
            })
        
        completed_lessons = UserLessonProgress.objects.filter(
            user_id=user_id,
            status='completed'
        ).count()
        
        completed_modules = UserModuleProgress.objects.filter(
            user_id=user_id,
            is_completed=True
        ).count()
        
        return Response({
            'total_modules': Module.objects.filter(is_published=True).count(),
            'total_lessons': Lesson.objects.filter(is_published=True).count(),
            'completed_modules': completed_modules,
            'completed_lessons': completed_lessons,
        })