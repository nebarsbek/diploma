import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { CartProvider } from './context/CartContext';
import { AuthProvider } from './context/AuthContext';
import { Navbar } from './components/Navbar';
import { Hero } from './components/Hero';
import { Menu } from './components/Menu';
import { CartSidebar } from './components/CartSidebar';
import { Footer } from './components/Footer';
import { Admin } from './pages/Admin';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { Profile } from './pages/Profile';
import { VerifyEmail } from './pages/VerifyEmail';
import { ProtectedRoute } from './components/ProtectedRoute';
import { ForgotPassword } from './pages/ForgotPassword';
import { ResetPassword } from './pages/ResetPassword';

const Home = () => (
  <div className="min-h-screen bg-gray-50">
    <Navbar />
    <Hero />
    <Menu />
    <CartSidebar />
    <Footer />
  </div>
);

function App() {
  return (
    <AuthProvider>
      <CartProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/admin" element={<Admin />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
            <Route path="/verify-email" element={<VerifyEmail />} />
            <Route path="/forgot-password" element={<ForgotPassword />} />
            <Route path="/reset-password" element={<ResetPassword />} />
          </Routes>
        </BrowserRouter>
      </CartProvider>
    </AuthProvider>
  );
}

export default App
