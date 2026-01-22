import { NavLink, Link } from 'react-router-dom';
import { 
  BookOpen, 
  TrendingUp, 
  Trophy, 
  Flame,
  Target,
  User,
  LogIn,
  LogOut
} from 'lucide-react';
import clsx from 'clsx';
import translations from '../i18n/translations';
import { useAuth } from '../contexts/AuthContext';

function Sidebar() {
  const { nav, user: userText, appName, auth: authText } = translations;
  const { user, isAuthenticated, logout, loading } = useAuth();
  
  // Default stats for non-authenticated users
  const displayUser = isAuthenticated && user ? {
    name: user.username,
    level: user.level || 1,
    xp: user.xp_points || 0,
    xpToNextLevel: user.xp_to_next_level || 1000,
    streak: user.streak_days || 0,
  } : {
    name: userText.student,
    level: 1,
    xp: 0,
    xpToNextLevel: 1000,
    streak: 0,
  };

  const navItems = [
    {
      to: '/',
      icon: BookOpen,
      label: nav.learningModules,
      description: nav.learningModulesDesc,
    },
    {
      to: '/simulation',
      icon: TrendingUp,
      label: nav.stockSimulation,
      description: nav.stockSimulationDesc,
    },
  ];

  const handleLogout = () => {
    logout();
  };

  return (
    <aside className="fixed left-0 top-0 h-screen w-64 bg-white border-r border-gray-200 flex flex-col">
      {/* Logo */}
      <div className="p-6 border-b border-gray-100">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-primary-500 rounded-xl flex items-center justify-center">
            <span className="text-white font-bold text-xl">$</span>
          </div>
          <div>
            <h1 className="text-xl font-bold text-gray-900">{appName}</h1>
          </div>
        </div>
      </div>

      {/* User Stats / Login Prompt */}
      <div className="p-4 border-b border-gray-100">
        {loading ? (
          // Loading state
          <div className="bg-gray-100 rounded-xl p-4 animate-pulse">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-10 h-10 bg-gray-200 rounded-full" />
              <div className="flex-1">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-2" />
                <div className="h-3 bg-gray-200 rounded w-1/2" />
              </div>
            </div>
          </div>
        ) : isAuthenticated ? (
          // Logged in - show user stats
          <div className="bg-gradient-to-r from-primary-50 to-accent-50 rounded-xl p-4">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-10 h-10 bg-primary-500 rounded-full flex items-center justify-center">
                <User className="w-5 h-5 text-white" />
              </div>
              <div>
                <p className="font-semibold text-gray-900">{displayUser.name}</p>
                <p className="text-sm text-gray-500">{userText.level} {displayUser.level}</p>
              </div>
            </div>
            
            {/* XP Progress */}
            <div className="mb-3">
              <div className="flex justify-between text-xs text-gray-600 mb-1">
                <span className="flex items-center gap-1">
                  <Target className="w-3 h-3" />
                  {displayUser.xp} {userText.xp}
                </span>
                <span>{displayUser.xpToNextLevel} {userText.toNextLevel}</span>
              </div>
              <div className="progress-bar">
                <div 
                  className="progress-fill"
                  style={{ width: `${(displayUser.xp % 1000) / 10}%` }}
                />
              </div>
            </div>

            {/* Streak */}
            <div className="flex items-center gap-2">
              <div className="streak-badge">
                <Flame className="w-4 h-4" />
                <span>{displayUser.streak} {userText.dayStreak}</span>
              </div>
            </div>
          </div>
        ) : (
          // Not logged in - show login prompt
          <div className="bg-gradient-to-r from-gray-50 to-gray-100 rounded-xl p-4">
            <p className="text-sm text-gray-600 mb-3">
              Inicia sesión para guardar tu progreso
            </p>
            <div className="flex flex-col gap-2">
              <Link 
                to="/login" 
                className="btn btn-primary py-2 text-sm flex items-center justify-center gap-2"
              >
                <LogIn className="w-4 h-4" />
                {authText.login}
              </Link>
              <Link 
                to="/register" 
                className="btn btn-outline py-2 text-sm flex items-center justify-center gap-2"
              >
                {authText.register}
              </Link>
            </div>
          </div>
        )}
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4">
        <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">
          {nav.modes}
        </p>
        <ul className="space-y-2">
          {navItems.map((item) => (
            <li key={item.to}>
              <NavLink
                to={item.to}
                className={({ isActive }) =>
                  clsx(
                    'flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200',
                    isActive
                      ? 'bg-primary-500 text-white shadow-lg shadow-primary-500/30'
                      : 'text-gray-600 hover:bg-gray-100'
                  )
                }
              >
                {({ isActive }) => (
                  <>
                    <item.icon className={clsx('w-5 h-5', isActive ? 'text-white' : 'text-gray-400')} />
                    <div>
                      <p className="font-medium">{item.label}</p>
                      <p className={clsx('text-xs', isActive ? 'text-primary-100' : 'text-gray-400')}>
                        {item.description}
                      </p>
                    </div>
                  </>
                )}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>

      {/* Bottom Section: Achievements & Logout */}
      <div className="p-4 border-t border-gray-100 space-y-3">
        {/* Achievements */}
        <div className="flex items-center gap-2 text-gray-600 hover:text-primary-500 cursor-pointer transition-colors">
          <Trophy className="w-5 h-5 text-secondary-500" />
          <span className="text-sm font-medium">{nav.achievements}</span>
          <span className="ml-auto bg-secondary-100 text-secondary-700 text-xs font-semibold px-2 py-1 rounded-full">
            {isAuthenticated ? '0/12' : '0/12'}
          </span>
        </div>

        {/* Logout button (only when authenticated) */}
        {isAuthenticated && (
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-2 px-4 py-2 text-gray-600 hover:text-red-500 hover:bg-red-50 rounded-xl transition-colors"
          >
            <LogOut className="w-4 h-4" />
            <span className="text-sm font-medium">{authText.logout}</span>
          </button>
        )}
      </div>
    </aside>
  );
}

export default Sidebar;
