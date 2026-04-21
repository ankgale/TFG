import { Link } from 'react-router-dom';
import { ChevronRight, BookOpen, Award, CheckCircle2 } from 'lucide-react';
import clsx from 'clsx';
import translations from '../i18n/translations';

function ModuleCard({ module, progress = 0, completedLessonIds = new Set() }) {
  const { module: moduleText } = translations;
  
  const difficultyColors = {
    beginner: 'bg-green-100 text-green-700',
    intermediate: 'bg-yellow-100 text-yellow-700',
    advanced: 'bg-red-100 text-red-700',
  };

  const getDifficultyLabel = (difficulty) => {
    return moduleText.difficulty[difficulty] || difficulty;
  };

  return (
    <Link
      to={`/module/${module.id}`}
      className="card-hover group block"
      style={{ borderLeftColor: module.color, borderLeftWidth: '4px' }}
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div 
            className="w-12 h-12 rounded-xl flex items-center justify-center text-2xl"
            style={{ backgroundColor: `${module.color}20` }}
          >
            {module.icon}
          </div>
          <div>
            <h3 className="font-bold text-gray-900 group-hover:text-primary-600 transition-colors">
              {module.title}
            </h3>
            <span className={clsx(
              'text-xs font-medium px-2 py-0.5 rounded-full',
              difficultyColors[module.difficulty] || difficultyColors.beginner
            )}>
              {getDifficultyLabel(module.difficulty)}
            </span>
          </div>
        </div>
        <ChevronRight className="w-5 h-5 text-gray-400 group-hover:text-primary-500 group-hover:translate-x-1 transition-all" />
      </div>

      <p className="text-gray-600 text-sm mb-4 line-clamp-2">
        {module.description}
      </p>

      {/* Stats */}
      <div className="flex items-center gap-4 text-sm text-gray-500 mb-4">
        <div className="flex items-center gap-1">
          <BookOpen className="w-4 h-4" />
          <span>{module.lessons_count || module.lessons?.length || 0} {moduleText.lessons}</span>
        </div>
        <div className="flex items-center gap-1">
          <Award className="w-4 h-4 text-secondary-500" />
          <span>{module.xp_reward} XP</span>
        </div>
      </div>

      {/* Progress bar */}
      <div>
        <div className="flex justify-between text-xs text-gray-500 mb-1">
          <span>{moduleText.progress}</span>
          <span>{progress}%</span>
        </div>
        <div className="progress-bar">
          <div 
            className="progress-fill"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Lessons preview */}
      {module.lessons && module.lessons.length > 0 && (
        <div className="mt-4 pt-4 border-t border-gray-100">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">
            {moduleText.lessons.charAt(0).toUpperCase() + moduleText.lessons.slice(1)}
          </p>
          <ul className="space-y-1">
            {module.lessons.slice(0, 3).map((lesson, index) => {
              const isCompleted = completedLessonIds.has(lesson.id);
              return (
                <li key={lesson.id}>
                  <span className="flex items-center gap-2 text-sm text-gray-600 py-1">
                    <span className={clsx(
                      'w-5 h-5 rounded-full flex items-center justify-center text-xs font-medium',
                      isCompleted
                        ? 'bg-green-500 text-white'
                        : 'bg-gray-100',
                    )}>
                      {isCompleted ? <CheckCircle2 className="w-3 h-3" /> : index + 1}
                    </span>
                    <span className="truncate">{lesson.title}</span>
                    {!isCompleted && (
                      <span className="ml-auto xp-badge text-xs">
                        +{lesson.xp_reward} XP
                      </span>
                    )}
                  </span>
                </li>
              );
            })}
            {module.lessons.length > 3 && (
              <li className="text-xs text-gray-400 pl-7">
                +{module.lessons.length - 3} {moduleText.moreLessons}
              </li>
            )}
          </ul>
        </div>
      )}
    </Link>
  );
}

export default ModuleCard;
