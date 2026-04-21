import { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { ArrowLeft, CheckCircle2, Lock, BookOpen, Award, Zap } from 'lucide-react';
import clsx from 'clsx';
import { lessonsApi } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import translations from '../i18n/translations';

function ModuleDetail() {
  const { moduleId } = useParams();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const { module: moduleText, lesson: lessonText } = translations;

  const [module, setModule] = useState(null);
  const [completedLessons, setCompletedLessons] = useState(new Set());
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [moduleData, completed] = await Promise.all([
          lessonsApi.getModule(moduleId),
          isAuthenticated
            ? lessonsApi.getCompletedLessons().catch(() => [])
            : Promise.resolve([]),
        ]);
        setModule(moduleData);
        setCompletedLessons(new Set(completed));
      } catch (error) {
        console.error('Failed to fetch module:', error);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [moduleId, isAuthenticated]);

  if (loading) {
    return (
      <div className="max-w-3xl mx-auto animate-pulse">
        <div className="h-8 bg-gray-200 rounded w-1/4 mb-4" />
        <div className="h-12 bg-gray-200 rounded w-3/4 mb-8" />
        <div className="space-y-4">
          {[1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="h-20 bg-gray-200 rounded-xl" />
          ))}
        </div>
      </div>
    );
  }

  if (!module) {
    return (
      <div className="max-w-3xl mx-auto text-center py-12">
        <p className="text-gray-500">Módulo no encontrado</p>
        <Link to="/" className="btn btn-primary mt-4">
          {lessonText.backToModules}
        </Link>
      </div>
    );
  }

  const lessons = module.lessons || [];
  const completedCount = lessons.filter((l) => completedLessons.has(l.id)).length;
  const progressPct = lessons.length ? Math.round((completedCount / lessons.length) * 100) : 0;

  const nextLesson = lessons.find((l) => !completedLessons.has(l.id));

  return (
    <div className="max-w-3xl mx-auto">
      {/* Header */}
      <div className="flex items-center gap-4 mb-6">
        <button
          onClick={() => navigate('/')}
          className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <ArrowLeft className="w-5 h-5 text-gray-600" />
        </button>
        <div
          className="w-14 h-14 rounded-xl flex items-center justify-center text-3xl"
          style={{ backgroundColor: `${module.color}20` }}
        >
          {module.icon}
        </div>
        <div className="flex-1">
          <h1 className="text-2xl font-bold text-gray-900">{module.title}</h1>
          <div className="flex items-center gap-3 text-sm text-gray-500 mt-1">
            <span className={clsx(
              'text-xs font-medium px-2 py-0.5 rounded-full',
              module.difficulty === 'beginner' && 'bg-green-100 text-green-700',
              module.difficulty === 'intermediate' && 'bg-yellow-100 text-yellow-700',
              module.difficulty === 'advanced' && 'bg-red-100 text-red-700',
            )}>
              {moduleText.difficulty[module.difficulty] || module.difficulty}
            </span>
            <span className="flex items-center gap-1">
              <BookOpen className="w-4 h-4" />
              {lessons.length} {moduleText.lessons}
            </span>
            <span className="flex items-center gap-1">
              <Award className="w-4 h-4 text-secondary-500" />
              {module.xp_reward} XP
            </span>
          </div>
        </div>
      </div>

      {/* Description */}
      <p className="text-gray-600 mb-6">{module.description}</p>

      {/* Overall progress */}
      <div className="card mb-6">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-gray-700">{moduleText.progress}</span>
          <span className="text-sm font-bold text-primary-600">{progressPct}%</span>
        </div>
        <div className="progress-bar">
          <div className="progress-fill" style={{ width: `${progressPct}%` }} />
        </div>
        <p className="text-xs text-gray-500 mt-2">
          {completedCount} / {lessons.length} {moduleText.lessons} completadas
        </p>
      </div>

      {/* Continue button */}
      {nextLesson && (
        <Link
          to={`/lesson/${nextLesson.id}`}
          className="btn btn-primary w-full py-3 mb-6 flex items-center justify-center gap-2"
        >
          <BookOpen className="w-5 h-5" />
          {completedCount === 0 ? 'Empezar Módulo' : 'Continuar Aprendiendo'}
        </Link>
      )}
      {!nextLesson && lessons.length > 0 && (
        <div className="bg-green-50 border border-green-200 rounded-xl p-4 mb-6 text-center text-green-700 font-semibold flex items-center justify-center gap-2">
          <CheckCircle2 className="w-5 h-5" />
          ¡Módulo completado!
        </div>
      )}

      {/* Lesson list */}
      <div className="space-y-3">
        {lessons.map((lesson, index) => {
          const isCompleted = completedLessons.has(lesson.id);
          return (
            <Link
              key={lesson.id}
              to={`/lesson/${lesson.id}`}
              className={clsx(
                'flex items-center gap-4 p-4 rounded-xl border-2 transition-all hover:shadow-md',
                isCompleted
                  ? 'border-green-200 bg-green-50/50'
                  : 'border-gray-200 hover:border-primary-300 bg-white',
              )}
            >
              <div
                className={clsx(
                  'w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold shrink-0',
                  isCompleted
                    ? 'bg-green-500 text-white'
                    : 'bg-gray-100 text-gray-600',
                )}
              >
                {isCompleted ? (
                  <CheckCircle2 className="w-5 h-5" />
                ) : (
                  index + 1
                )}
              </div>

              <div className="flex-1 min-w-0">
                <p className={clsx(
                  'font-semibold truncate',
                  isCompleted ? 'text-green-700' : 'text-gray-900',
                )}>
                  {lesson.title}
                </p>
                {lesson.description && (
                  <p className="text-sm text-gray-500 truncate">{lesson.description}</p>
                )}
              </div>

              {!isCompleted && (
                <span className="xp-badge text-xs shrink-0">
                  <Zap className="w-3 h-3" />
                  +{lesson.xp_reward} XP
                </span>
              )}
              {isCompleted && (
                <span className="text-xs font-medium text-green-600 shrink-0">Completada</span>
              )}
            </Link>
          );
        })}
      </div>
    </div>
  );
}

export default ModuleDetail;
