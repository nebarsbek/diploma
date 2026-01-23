import { useState } from 'react';
import { Plus } from 'lucide-react';
import type { Pizza } from '../types';
import { useCart } from '../context/CartContext';

interface ProductCardProps {
  pizza: Pizza;
}

export const ProductCard = ({ pizza }: ProductCardProps) => {
  const [size, setSize] = useState<'30cm' | '40cm'>('30cm');
  const { addToCart } = useCart();

  const isPizza = pizza.category === 'pizza';
  const currentPrice = (isPizza && size === '40cm') ? Number(pizza.price) * 1.3 : Number(pizza.price);

  return (
    <div className="bg-white rounded-2xl overflow-hidden shadow-lg hover:shadow-xl transition-shadow duration-300 border border-gray-100 flex flex-col h-full">
      <div className="h-48 overflow-hidden relative group">
        <img 
          src={pizza.image_url || 'https://placehold.co/600x400?text=No+Image'} 
          alt={pizza.name} 
          className="w-full h-full object-cover transform group-hover:scale-110 transition-transform duration-500"
        />
      </div>
      
      <div className="p-5 flex flex-col flex-grow">
        <h3 className="text-xl font-bold text-gray-900 mb-2">{pizza.name}</h3>
        <p className="text-gray-500 text-sm mb-4 flex-grow line-clamp-3">{pizza.description}</p>
        
        <div className="mt-auto space-y-4">
          {isPizza && (
            <div className="flex bg-gray-100 rounded-lg p-1">
              {(['30cm', '40cm'] as const).map((s) => (
                <button
                  key={s}
                  onClick={() => setSize(s)}
                  className={`flex-1 py-1 text-sm font-medium rounded-md transition-all ${
                    size === s ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  {s}
                </button>
              ))}
            </div>
          )}
          
          <div className="flex items-center justify-between">
            <span className="text-2xl font-bold text-gray-900">${currentPrice.toFixed(2)}</span>
            <button 
              onClick={() => addToCart(pizza, size)}
              className="bg-primary hover:bg-orange-700 text-white p-2 rounded-full transition-colors"
            >
              <Plus size={24} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};