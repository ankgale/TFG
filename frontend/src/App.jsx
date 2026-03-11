import { Routes, Route } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import Layout from './components/Layout'
import ProtectedRoute from './components/ProtectedRoute'
import Dashboard from './pages/Dashboard'
import LessonDetail from './pages/LessonDetail'
import StockSimulation from './pages/StockSimulation'
import Achievements from './pages/Achievements'
import TransactionHistory from './pages/TransactionHistory'
import Profile from './pages/Profile'
import Leaderboard from './pages/Leaderboard'
import Login from './pages/Login'
import Register from './pages/Register'

function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="lesson/:lessonId" element={<LessonDetail />} />
          <Route path="simulation" element={<ProtectedRoute><StockSimulation /></ProtectedRoute>} />
          <Route path="achievements" element={<Achievements />} />
          <Route path="transactions" element={<ProtectedRoute><TransactionHistory /></ProtectedRoute>} />
          <Route path="profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
          <Route path="leaderboard" element={<Leaderboard />} />
        </Route>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </AuthProvider>
  )
}

export default App
