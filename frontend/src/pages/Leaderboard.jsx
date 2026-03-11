import { useState, useEffect } from 'react';
import { Trophy, Medal, Flame, Loader2 } from 'lucide-react';
import clsx from 'clsx';
import { usersApi } from '../services/api';
import { useAuth } from '../contexts/AuthContext';

const PODIUM_COLORS = [
  'from-yellow-400 to-yellow-500',
  'from-gray-300 to-gray-400',
  'from-amber-600 to-amber-700',
];

function Leaderboard() {
  const { user } = useAuth();
  const [leaders, setLeaders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchLeaderboard() {
      try {
        const data = await usersApi.getLeaderboard();
        setLeaders(data ?? []);
      } catch (err) {
        console.log('Leaderboard fetch failed:', err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchLeaderboard();
  }, []);

  return (
    <div className="max-w-2xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-1">Clasificación</h1>
          <p className="text-gray-500">Los mejores estudiantes de FinLearn</p>
        </div>
        <div className="w-14 h-14 bg-yellow-100 rounded-2xl flex items-center justify-center">
          <Trophy className="w-7 h-7 text-yellow-500" />
        </div>
      </div>

      {loading ? (
        <div className="flex flex-col items-center justify-center py-20">
          <Loader2 className="w-10 h-10 text-primary-500 animate-spin mb-3" />
          <p className="text-sm text-gray-500">Cargando...</p>
        </div>
      ) : leaders.length === 0 ? (
        <div className="card text-center py-16 text-gray-400">
          Aún no hay usuarios en la clasificación.
        </div>
      ) : (
        <>
          {/* Top 3 podium */}
          {leaders.length >= 3 && (
            <div className="grid grid-cols-3 gap-3 mb-8">
              {[1, 0, 2].map((idx) => {
                const l = leaders[idx];
                if (!l) return null;
                const isFirst = idx === 0;
                return (
                  <div
                    key={l.username}
                    className={clsx(
                      'card text-center py-6',
                      isFirst && 'ring-2 ring-yellow-400 scale-105'
                    )}
                  >
                    <div
                      className={clsx(
                        'w-12 h-12 mx-auto rounded-full flex items-center justify-center text-white font-bold text-lg mb-2 bg-gradient-to-b',
                        PODIUM_COLORS[idx],
                      )}
                    >
                      {l.rank}
                    </div>
                    <p className={clsx(
                      'font-semibold truncate px-2',
                      user?.username === l.username ? 'text-primary-600' : 'text-gray-900'
                    )}>
                      {l.username}
                    </p>
                    <p className="text-sm text-gray-500">Nivel {l.level}</p>
                    <p className="text-lg font-bold text-primary-600 mt-1">{l.xp_points.toLocaleString()} XP</p>
                  </div>
                );
              })}
            </div>
          )}

          {/* Full list */}
          <div className="space-y-2">
            {leaders.map((l) => (
              <div
                key={l.username}
                className={clsx(
                  'card flex items-center gap-4 py-3',
                  user?.username === l.username && 'ring-2 ring-primary-300 bg-primary-50/40'
                )}
              >
                <div className="w-8 text-center">
                  {l.rank <= 3 ? (
                    <Medal className={clsx('w-5 h-5 mx-auto', l.rank === 1 ? 'text-yellow-500' : l.rank === 2 ? 'text-gray-400' : 'text-amber-600')} />
                  ) : (
                    <span className="text-sm font-semibold text-gray-400">{l.rank}</span>
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <p className={clsx('font-semibold truncate', user?.username === l.username ? 'text-primary-600' : 'text-gray-900')}>
                    {l.username}
                    {user?.username === l.username && <span className="text-xs ml-1 text-primary-400">(tú)</span>}
                  </p>
                  <p className="text-xs text-gray-400">Nivel {l.level}</p>
                </div>
                <div className="flex items-center gap-3 flex-shrink-0">
                  {l.streak_days > 0 && (
                    <span className="flex items-center gap-1 text-xs text-orange-500">
                      <Flame className="w-3.5 h-3.5" />
                      {l.streak_days}
                    </span>
                  )}
                  <span className="font-bold text-primary-600">{l.xp_points.toLocaleString()} XP</span>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

export default Leaderboard;
