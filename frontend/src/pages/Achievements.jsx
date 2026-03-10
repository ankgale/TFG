import { useState, useEffect } from 'react';
import { Trophy, Lock, CheckCircle, Loader2 } from 'lucide-react';
import clsx from 'clsx';
import { usersApi } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import translations from '../i18n/translations';

const CATEGORY_META = {
  learning: { label: 'Aprendizaje', color: 'bg-primary-100 text-primary-700' },
  trading: { label: 'Trading', color: 'bg-green-100 text-green-700' },
  streak: { label: 'Racha', color: 'bg-orange-100 text-orange-700' },
  special: { label: 'Especial', color: 'bg-purple-100 text-purple-700' },
};

function Achievements() {
  const { isAuthenticated } = useAuth();
  const [allAchievements, setAllAchievements] = useState([]);
  const [unlockedIds, setUnlockedIds] = useState(new Set());
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    async function fetchData() {
      try {
        const all = await usersApi.getAchievements();
        setAllAchievements(all?.results ?? all ?? []);

        if (isAuthenticated) {
          const unlocked = await usersApi.getUserAchievements();
          const list = unlocked?.results ?? unlocked ?? [];
          setUnlockedIds(new Set(list.map((ua) => ua.achievement.id)));
        }
      } catch (err) {
        console.log('Failed to fetch achievements:', err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [isAuthenticated]);

  const categories = ['all', ...Object.keys(CATEGORY_META)];

  const filtered = filter === 'all'
    ? allAchievements
    : allAchievements.filter((a) => a.category === filter);

  const unlockedCount = allAchievements.filter((a) => unlockedIds.has(a.id)).length;

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-1">
            {translations.nav.achievements}
          </h1>
          <p className="text-gray-500">
            {unlockedCount} / {allAchievements.length} desbloqueados
          </p>
        </div>
        <div className="w-14 h-14 bg-secondary-100 rounded-2xl flex items-center justify-center">
          <Trophy className="w-7 h-7 text-secondary-500" />
        </div>
      </div>

      {/* Category filter pills */}
      <div className="flex flex-wrap gap-2 mb-6">
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => setFilter(cat)}
            className={clsx(
              'px-4 py-1.5 rounded-full text-sm font-medium transition-colors',
              filter === cat
                ? 'bg-primary-500 text-white'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            )}
          >
            {cat === 'all' ? 'Todos' : CATEGORY_META[cat]?.label ?? cat}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="flex flex-col items-center justify-center py-20">
          <Loader2 className="w-10 h-10 text-primary-500 animate-spin mb-3" />
          <p className="text-sm text-gray-500">{translations.common.loading}</p>
        </div>
      ) : filtered.length === 0 ? (
        <div className="text-center py-20 text-gray-400">
          No hay logros en esta categoría.
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {filtered.map((achievement) => {
            const unlocked = unlockedIds.has(achievement.id);
            const meta = CATEGORY_META[achievement.category];
            return (
              <div
                key={achievement.id}
                className={clsx(
                  'card flex items-start gap-4 transition-all',
                  unlocked
                    ? 'border-2 border-secondary-300 bg-secondary-50/40'
                    : 'opacity-70 grayscale'
                )}
              >
                <div className="text-3xl flex-shrink-0 mt-0.5">
                  {achievement.icon}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <h3 className="font-semibold text-gray-900 truncate">
                      {achievement.name}
                    </h3>
                    {unlocked ? (
                      <CheckCircle className="w-4 h-4 text-green-500 flex-shrink-0" />
                    ) : (
                      <Lock className="w-4 h-4 text-gray-400 flex-shrink-0" />
                    )}
                  </div>
                  <p className="text-sm text-gray-500 mb-2">
                    {achievement.description}
                  </p>
                  <div className="flex items-center gap-2">
                    {meta && (
                      <span className={clsx('text-xs px-2 py-0.5 rounded-full font-medium', meta.color)}>
                        {meta.label}
                      </span>
                    )}
                    <span className="text-xs text-secondary-600 font-medium">
                      +{achievement.xp_reward} XP
                    </span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default Achievements;
