import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/useAuth';

export const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login(email, password);
      navigate('/');
    } catch (error) {
      alert('Login failed');
      console.log(error);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white p-8 rounded-xl shadow-md w-96">
        <h2 className="text-2xl font-bold mb-6 text-center">Login</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input type="email" required className="w-full p-2 border rounded" value={email} onChange={e => setEmail(e.target.value)} />
          </div>
          <div>
            <div className="flex justify-between items-center mb-1">
              <label className="block text-sm font-medium text-gray-700">Password</label>
              <Link to="/forgot-password" className="text-xs text-primary hover:underline">Forgot Password?</Link>
            </div>
            <input type="password" required className="w-full p-2 border rounded" value={password} onChange={e => setPassword(e.target.value)} />
          </div>
          <button type="submit" className="w-full bg-primary text-white py-2 rounded font-bold hover:bg-orange-700">
            Login
          </button>
        </form>
        <p className="mt-4 text-center text-sm text-gray-600">Don't have an account? <Link to="/register" className="text-primary hover:underline">Register</Link></p>
      </div>
    </div>
  );
};
