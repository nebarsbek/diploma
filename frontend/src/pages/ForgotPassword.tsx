import { useState } from 'react';
import { Link } from 'react-router-dom';
import { forgotPassword } from '../api/auth';

export const ForgotPassword = () => {
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus('loading');
    try {
      await forgotPassword(email);
      setStatus('success');
    } catch {
      setStatus('error');
    }
  };

  if (status === 'success') {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="bg-white p-8 rounded-xl shadow-md w-96 text-center">
          <h2 className="text-2xl font-bold mb-4">Check your email</h2>
          <p className="text-gray-600 mb-6">We have sent a password reset link to {email}</p>
          <Link to="/login" className="text-primary hover:underline">Back to Login</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white p-8 rounded-xl shadow-md w-96">
        <h2 className="text-2xl font-bold mb-6 text-center">Reset Password</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input type="email" required className="w-full p-2 border rounded" value={email} onChange={e => setEmail(e.target.value)} />
          </div>
          <button type="submit" disabled={status === 'loading'} className="w-full bg-primary text-white py-2 rounded font-bold hover:bg-orange-700 disabled:opacity-50">
            {status === 'loading' ? 'Sending...' : 'Send Reset Link'}
          </button>
        </form>
        <div className="mt-4 text-center"><Link to="/login" className="text-sm text-gray-600 hover:text-gray-900">Back to Login</Link></div>
      </div>
    </div>
  );
};
