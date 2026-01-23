import { ShoppingCart, User, LogOut } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/useAuth';

export const Navbar = () => {
  const { toggleCart, items } = useCart();
  const { user, logout } = useAuth();
  const itemCount = items.reduce((acc, item) => acc + item.quantity, 0);

  return (
    <nav className="fixed top-0 left-0 right-0 bg-white/95 backdrop-blur-sm shadow-sm z-50 h-16">
      <div className="max-w-7xl mx-auto px-4 h-full flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center gap-2">
          <Link to="/" className="text-2xl font-bold text-gray-900">PIZZA<span className="text-primary">DELIVERY</span></Link>
        </div>

        {/* Navigation Links */}
        <div className="hidden md:flex items-center gap-8 font-medium text-gray-600">
          <a href="#pizza" className="hover:text-primary transition-colors">Pizza</a>
          <a href="#drinks" className="hover:text-primary transition-colors">Drinks</a>
          <a href="#desserts" className="hover:text-primary transition-colors">Desserts</a>
        </div>

        {/* Actions */}
        <div className="flex items-center gap-4">
          {user ? (
            <div className="flex items-center gap-4">
              <Link to="/profile" className="text-sm font-medium text-gray-700 hidden sm:block hover:text-primary transition-colors">
                {user.email}
              </Link>
              {['admin', 'employee'].includes(user.role) && (
                <Link to="/admin" className="text-sm font-medium text-gray-600 hover:text-primary">Admin Panel</Link>
              )}
              <button onClick={logout} className="p-2 text-gray-600 hover:text-red-600 transition-colors" title="Logout">
                <LogOut size={20} />
              </button>
            </div>
          ) : (
            <Link to="/login" className="flex items-center gap-2 text-gray-600 hover:text-primary font-medium">
              <User size={20} /> Login
            </Link>
          )}
          <button 
            onClick={toggleCart}
            className="relative p-2 bg-primary text-white rounded-full hover:bg-orange-700 transition-colors"
          >
            <ShoppingCart size={20} />
            {itemCount > 0 && (
              <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs font-bold w-5 h-5 rounded-full flex items-center justify-center border-2 border-white">
                {itemCount}
              </span>
            )}
          </button>
        </div>
      </div>
    </nav>
  );
};