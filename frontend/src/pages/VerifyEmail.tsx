import { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { api } from '../api/client';

export const VerifyEmail = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const token = searchParams.get('token');
  const [status, setStatus] = useState<'verifying' | 'success' | 'error'>(token ? 'verifying' : 'error');

  useEffect(() => {
    if (!token) {
      return;
    }

    api.post(`/auth/verify-email?token=${token}`)
      .then(() => {
        setStatus('success');
        setTimeout(() => navigate('/login'), 3000);
      })
      .catch(() => {
        setStatus('error');
      });
  }, [token, navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white p-8 rounded-xl shadow-md text-center max-w-md">
        {status === 'verifying' && <h2 className="text-2xl font-bold">Verifying your email...</h2>}
        {status === 'success' && (
          <div>
            <h2 className="text-2xl font-bold text-green-600 mb-2">Email Verified!</h2>
            <p>Redirecting to login...</p>
          </div>
        )}
        {status === 'error' && (
          <h2 className="text-2xl font-bold text-red-600">Verification failed. Invalid or expired token.</h2>
        )}
      </div>
    </div>
  );
};
