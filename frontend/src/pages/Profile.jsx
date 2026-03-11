import { useState } from 'react';
import { User, Mail, FileText, Lock, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { usersApi } from '../services/api';

function Profile() {
  const { user, refreshUser } = useAuth();

  const [profileData, setProfileData] = useState({
    email: user?.email || '',
    bio: user?.bio || '',
  });
  const [passwords, setPasswords] = useState({
    current_password: '',
    new_password: '',
    confirm_password: '',
  });
  const [profileMsg, setProfileMsg] = useState({ type: '', text: '' });
  const [passwordMsg, setPasswordMsg] = useState({ type: '', text: '' });
  const [savingProfile, setSavingProfile] = useState(false);
  const [savingPassword, setSavingPassword] = useState(false);

  const handleProfileChange = (e) => {
    setProfileData({ ...profileData, [e.target.name]: e.target.value });
    setProfileMsg({ type: '', text: '' });
  };

  const handlePasswordChange = (e) => {
    setPasswords({ ...passwords, [e.target.name]: e.target.value });
    setPasswordMsg({ type: '', text: '' });
  };

  const handleProfileSubmit = async (e) => {
    e.preventDefault();
    setSavingProfile(true);
    setProfileMsg({ type: '', text: '' });
    try {
      await usersApi.updateProfile(profileData);
      await refreshUser();
      setProfileMsg({ type: 'success', text: 'Perfil actualizado correctamente' });
    } catch (err) {
      setProfileMsg({ type: 'error', text: err.message || 'Error al actualizar el perfil' });
    } finally {
      setSavingProfile(false);
    }
  };

  const handlePasswordSubmit = async (e) => {
    e.preventDefault();
    setPasswordMsg({ type: '', text: '' });

    if (passwords.new_password !== passwords.confirm_password) {
      setPasswordMsg({ type: 'error', text: 'Las contraseñas no coinciden' });
      return;
    }
    if (passwords.new_password.length < 8) {
      setPasswordMsg({ type: 'error', text: 'La nueva contraseña debe tener al menos 8 caracteres' });
      return;
    }

    setSavingPassword(true);
    try {
      const result = await usersApi.changePassword(
        passwords.current_password,
        passwords.new_password,
      );
      localStorage.setItem('token', result.token);
      setPasswords({ current_password: '', new_password: '', confirm_password: '' });
      setPasswordMsg({ type: 'success', text: 'Contraseña actualizada correctamente' });
    } catch (err) {
      setPasswordMsg({ type: 'error', text: err.message || 'Error al cambiar la contraseña' });
    } finally {
      setSavingPassword(false);
    }
  };

  const Feedback = ({ msg }) => {
    if (!msg.text) return null;
    const isError = msg.type === 'error';
    return (
      <div className={`flex items-center gap-2 p-3 rounded-xl text-sm ${isError ? 'bg-red-50 border border-red-200 text-red-700' : 'bg-green-50 border border-green-200 text-green-700'}`}>
        {isError ? <AlertCircle className="w-4 h-4 flex-shrink-0" /> : <CheckCircle className="w-4 h-4 flex-shrink-0" />}
        <span>{msg.text}</span>
      </div>
    );
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="flex items-center gap-4 mb-8">
        <div className="w-16 h-16 bg-primary-500 rounded-full flex items-center justify-center">
          <User className="w-8 h-8 text-white" />
        </div>
        <div>
          <h1 className="text-3xl font-bold text-gray-900">{user?.username}</h1>
          <p className="text-gray-500">Nivel {user?.level || 1} &middot; {user?.xp_points || 0} XP</p>
        </div>
      </div>

      {/* Profile info */}
      <div className="card mb-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <FileText className="w-5 h-5 text-primary-500" />
          Información del Perfil
        </h2>
        <form onSubmit={handleProfileSubmit} className="space-y-4">
          <Feedback msg={profileMsg} />
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              <span className="flex items-center gap-1"><Mail className="w-3.5 h-3.5" /> Correo electrónico</span>
            </label>
            <input
              type="email"
              name="email"
              value={profileData.email}
              onChange={handleProfileChange}
              placeholder="tu@email.com (opcional)"
              className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Bio</label>
            <textarea
              name="bio"
              value={profileData.bio}
              onChange={handleProfileChange}
              rows={3}
              maxLength={500}
              placeholder="Cuéntanos algo sobre ti..."
              className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 resize-none"
            />
            <p className="text-xs text-gray-400 mt-1 text-right">{profileData.bio.length}/500</p>
          </div>
          <button
            type="submit"
            disabled={savingProfile}
            className="btn btn-primary py-2.5 flex items-center justify-center gap-2 disabled:opacity-50"
          >
            {savingProfile ? <Loader2 className="w-4 h-4 animate-spin" /> : null}
            Guardar Cambios
          </button>
        </form>
      </div>

      {/* Change password */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <Lock className="w-5 h-5 text-primary-500" />
          Cambiar Contraseña
        </h2>
        <form onSubmit={handlePasswordSubmit} className="space-y-4">
          <Feedback msg={passwordMsg} />
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Contraseña actual</label>
            <input
              type="password"
              name="current_password"
              value={passwords.current_password}
              onChange={handlePasswordChange}
              required
              className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Nueva contraseña</label>
            <input
              type="password"
              name="new_password"
              value={passwords.new_password}
              onChange={handlePasswordChange}
              required
              minLength={8}
              className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Confirmar nueva contraseña</label>
            <input
              type="password"
              name="confirm_password"
              value={passwords.confirm_password}
              onChange={handlePasswordChange}
              required
              className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            />
          </div>
          <button
            type="submit"
            disabled={savingPassword}
            className="btn btn-primary py-2.5 flex items-center justify-center gap-2 disabled:opacity-50"
          >
            {savingPassword ? <Loader2 className="w-4 h-4 animate-spin" /> : null}
            Cambiar Contraseña
          </button>
        </form>
      </div>
    </div>
  );
}

export default Profile;
