import { useState, useEffect } from 'react';
import ModuleCard from '../components/ModuleCard';
import { lessonsApi } from '../services/api';
import translations from '../i18n/translations';

function Dashboard() {
  const { dashboard, sampleModules } = translations;
  const [modules, setModules] = useState(sampleModules);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const modulesData = await lessonsApi.getModules();
        if (modulesData && modulesData.length > 0) {
          setModules(modulesData);
        }
      } catch (error) {
        console.log('Using sample data:', error.message);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          {dashboard.title}
        </h1>
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
