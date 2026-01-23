import { Facebook, Instagram, Twitter, MapPin, Phone, Clock } from 'lucide-react';

export const Footer = () => {
  return (
    <footer className="bg-gray-900 text-white pt-16 pb-8">
      <div className="max-w-7xl mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-12 mb-12">
          <div>
            <h3 className="text-2xl font-bold mb-6">PIZZA<span className="text-primary">DELIVERY</span></h3>
            <p className="text-gray-400 leading-relaxed">
              The best pizza in town, made with love and fresh ingredients. Delivered hot to your door.
            </p>
          </div>
          
          <div>
            <h4 className="text-lg font-bold mb-6">Contact Us</h4>
            <ul className="space-y-4 text-gray-400">
              <li className="flex items-center gap-3"><MapPin size={20} className="text-primary" /> 123 Pizza Street, Food City</li>
              <li className="flex items-center gap-3"><Phone size={20} className="text-primary" /> +1 234 567 890</li>
              <li className="flex items-center gap-3"><Clock size={20} className="text-primary" /> Daily: 10:00 - 23:00</li>
            </ul>
          </div>

          <div>
            <h4 className="text-lg font-bold mb-6">Follow Us</h4>
            <div className="flex gap-4">
              <a href="#" className="bg-gray-800 p-3 rounded-full hover:bg-primary transition-colors"><Facebook size={20} /></a>
              <a href="#" className="bg-gray-800 p-3 rounded-full hover:bg-primary transition-colors"><Instagram size={20} /></a>
              <a href="#" className="bg-gray-800 p-3 rounded-full hover:bg-primary transition-colors"><Twitter size={20} /></a>
            </div>
          </div>
        </div>
        
        <div className="border-t border-gray-800 pt-8 text-center text-gray-500 text-sm">
          © 2026 Pizza Delivery. All rights reserved.
        </div>
      </div>
    </footer>
  );
};