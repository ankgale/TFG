"""
Lesson models for FinLearn.
Duolingo-style learning structure: Modules → Lessons → Content/Quizzes
"""

from django.db import models
from django.conf import settings


class Module(models.Model):
    """
    A learning module containing multiple lessons.
    Example: "Introduction to Investing", "Stock Market Basics"
    """
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='📚')  # Emoji or icon class
    color = models.CharField(max_length=7, default='#6366f1')  # Hex color
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    order = models.PositiveIntegerField(default=0)  # Display order
    xp_reward = models.PositiveIntegerField(default=500)  # XP for completing module
    
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'modules'
        ordering = ['order']
    
    def __str__(self):
        return self.title
    
    @property
    def lessons_count(self) -> int:
        return self.lessons.count()


class Lesson(models.Model):
    """
    A single lesson within a module.
    Contains educational content and quizzes.
    """
    
    module = models.ForeignKey(
        Module, 
        on_delete=models.CASCADE, 
        related_name='lessons'
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    content = models.TextField()  # Main lesson content (Markdown supported)
    order = models.PositiveIntegerField(default=0)
    xp_reward = models.PositiveIntegerField(default=50)  # XP for completing lesson
    
    # Estimated time in minutes
    estimated_time = models.PositiveIntegerField(default=5)
    
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'lessons'
        ordering = ['module', 'order']
    
    def __str__(self):
        return f"{self.module.title} - {self.title}"


class Quiz(models.Model):
    """
    Quiz questions for a lesson.
    Multiple choice format (Duolingo-style).
    """
    
    QUESTION_TYPE_CHOICES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('fill_blank', 'Fill in the Blank'),
    ]
    
    lesson = models.ForeignKey(
        Lesson, 
        on_delete=models.CASCADE, 
        related_name='quizzes'
    )
    
    question = models.TextField()
    question_type = models.CharField(
        max_length=20, 
        choices=QUESTION_TYPE_CHOICES, 
        default='multiple_choice'
    )
    explanation = models.TextField(blank=True)  # Shown after answering
    order = models.PositiveIntegerField(default=0)
    xp_reward = models.PositiveIntegerField(default=10)  # XP for correct answer
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'quizzes'
        ordering = ['lesson', 'order']
        verbose_name_plural = 'Quizzes'
    
    def __str__(self):
        return f"Quiz: {self.question[:50]}..."


class QuizOption(models.Model):
    """
    Answer options for a quiz question.
    """
    
    quiz = models.ForeignKey(
        Quiz, 
        on_delete=models.CASCADE, 
        related_name='options'
    )
    
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        db_table = 'quiz_options'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.text} ({'✓' if self.is_correct else '✗'})"


class UserLessonProgress(models.Model):
    """
    Track user progress through lessons.
    """
    
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lesson_progress',
        null=True,  # Nullable for now (no auth yet)
        blank=True
    )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    score = models.PositiveIntegerField(default=0)  # Quiz score percentage
    attempts = models.PositiveIntegerField(default=0)
    
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'user_lesson_progress'
        unique_together = ['user', 'lesson']
    
    def __str__(self):
        return f"{self.user} - {self.lesson} ({self.status})"


class UserModuleProgress(models.Model):
    """
    Track user progress through modules.
    """
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='module_progress',
        null=True,  # Nullable for now (no auth yet)
        blank=True
    )
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    
    lessons_completed = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'user_module_progress'
        unique_together = ['user', 'module']
    
    def __str__(self):
        return f"{self.user} - {self.module}"
    
    @property
    def progress_percentage(self) -> int:
        total = self.module.lessons_count
        if total == 0:
            return 0
        return int((self.lessons_completed / total) * 100)
