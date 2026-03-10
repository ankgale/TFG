import { Routes, Route } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import LessonDetail from './pages/LessonDetail'
import StockSimulation from './pages/StockSimulation'
import Achievements from './pages/Achievements'
import TransactionHistory from './pages/TransactionHistory'
import Login from './pages/Login'
import Register from './pages/Register'

function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="lesson/:lessonId" element={<LessonDetail />} />
          <Route path="simulation" element={<StockSimulation />} />
          <Route path="achievements" element={<Achievements />} />
          <Route path="transactions" element={<TransactionHistory />} />
        </Route>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </AuthProvider>
  )
}

export default App
