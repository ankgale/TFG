import { useState, useEffect } from 'react';
import { BookOpen, Target, Trophy, Zap } from 'lucide-react';
import ModuleCard from '../components/ModuleCard';
import { lessonsApi } from '../services/api';
import translations from '../i18n/translations';

function Dashboard() {
  const { dashboard, sampleModules } = translations;
  const [modules, setModules] = useState(sampleModules);
  const [loading, setLoading] = useState(true);
  const [progressSummary, setProgressSummary] = useState(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const [modulesData, progressData] = await Promise.all([
          lessonsApi.getModules(),
          lessonsApi.getProgressSummary(),
        ]);
        
        if (modulesData && modulesData.length > 0) {
          setModules(modulesData);
        }
        setProgressSummary(progressData);
      } catch (error) {
        console.log('Using sample data:', error.message);
        // Keep sample modules if API fails
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  const stats = [
    {
      label: dashboard.modulesAvailable,
      value: modules.length,
      icon: BookOpen,
      color: 'text-primary-500',
      bgColor: 'bg-primary-50',
    },
    {
      label: dashboard.totalLessons,
      value: modules.reduce((sum, m) => sum + (m.lessons_count || 0), 0),
      icon: Target,
      color: 'text-accent-500',
      bgColor: 'bg-accent-50',
    },
    {
      label: dashboard.xpAvailable,
      value: modules.reduce((sum, m) => sum + (m.xp_reward || 0), 0).toLocaleString(),
      icon: Zap,
      color: 'text-secondary-500',
      bgColor: 'bg-secondary-50',
    },
    {
      label: dashboard.completed,
      value: progressSummary?.completed_modules || 0,
      icon: Trophy,
      color: 'text-purple-500',
      bgColor: 'bg-purple-50',
    },
  ];

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          {dashboard.title}
        </h1>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {stats.map((stat) => (
          <div key={stat.label} className="card flex items-center gap-4">
            <div className={`w-12 h-12 ${stat.bgColor} rounded-xl flex items-center justify-center`}>
              <stat.icon className={`w-6 h-6 ${stat.color}`} />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
              <p className="text-sm text-gray-500">{stat.label}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Daily Challenge Banner */}
      <div className="bg-gradient-to-r from-primary-500 to-accent-500 rounded-2xl p-6 mb-8 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold mb-1">{dashboard.dailyChallenge}</h2>
            <p className="text-primary-100">
              {dashboard.dailyChallengeDesc}
            </p>
          </div>
          <div className="flex items-center gap-2">
            <div className="bg-white/20 rounded-xl px-4 py-2 backdrop-blur-sm">
              <p className="text-sm text-primary-100">{dashboard.progress}</p>
              <p className="text-2xl font-bold">0/3</p>
            </div>
            <button className="btn bg-white text-primary-600 hover:bg-primary-50">
              {dashboard.startLearning}
            </button>
          </div>
        </div>
      </div>

      {/* Module Grid */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="card animate-pulse">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-12 h-12 bg-gray-200 rounded-xl" />
                <div className="flex-1">
                  <div className="h-5 bg-gray-200 rounded w-3/4 mb-2" />
                  <div className="h-4 bg-gray-200 rounded w-1/4" />
                </div>
              </div>
              <div className="h-4 bg-gray-200 rounded w-full mb-2" />
              <div className="h-4 bg-gray-200 rounded w-2/3" />
            </div>
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {modules.map((module) => (
            <ModuleCard 
              key={module.id} 
              module={module} 
              progress={0} // Will be calculated from user progress when auth is implemented
            />
          ))}
        </div>
      )}

      {/* Coming Soon Section */}
      <div className="mt-12 text-center">
        <p className="text-gray-400 text-sm">
          {dashboard.moreModulesComingSoon}
        </p>
      </div>
    </div>
  );
}

export default Dashboard;
