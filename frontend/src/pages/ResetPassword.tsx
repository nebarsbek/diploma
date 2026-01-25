import { useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { resetPassword } from '../api/auth';

export const ResetPassword = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const token = searchParams.get('token');
  
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [status, setStatus] = useState<'idle' | 'loading' | 'error'>('idle');

  if (!token) {
    return <div className="min-h-screen flex items-center justify-center">Invalid token</div>;
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (newPassword !== confirmPassword) {
      alert("Passwords don't match");
      return;
    }
    
    setStatus('loading');
    try {
      await resetPassword(token, newPassword);
      alert('Password reset successfully');
      navigate('/login');
    } catch {
      setStatus('error');
      alert('Failed to reset password');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white p-8 rounded-xl shadow-md w-96">
        <h2 className="text-2xl font-bold mb-6 text-center">Set New Password</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">New Password</label>
            <input type="password" required className="w-full p-2 border rounded" value={newPassword} onChange={e => setNewPassword(e.target.value)} />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Confirm Password</label>
            <input type="password" required className="w-full p-2 border rounded" value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} />
          </div>
          <button type="submit" disabled={status === 'loading'} className="w-full bg-primary text-white py-2 rounded font-bold hover:bg-orange-700 disabled:opacity-50">
            {status === 'loading' ? 'Resetting...' : 'Reset Password'}
          </button>
        </form>
      </div>
    </div>
  );
};
