import { useEffect, useState } from 'react';
import { getPizzas } from '../api/pizzas';
import type { Pizza } from '../types';
import { ProductCard } from './ProductCard';

export const Menu = () => {
  const [pizzas, setPizzas] = useState<Pizza[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPizzas = async () => {
      try {
        const data = await getPizzas();
        setPizzas(data);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };
    fetchPizzas();
  }, []);

  const categories = [
    { id: 'pizza', name: 'Pizza' },
    { id: 'drinks', name: 'Drinks' },
    { id: 'desserts', name: 'Desserts' },
  ];

  return (
    <section id="menu" className="py-12 bg-gray-50 min-h-screen">
      {/* Sticky Category Nav */}
      <div className="sticky top-16 z-40 bg-white/95 backdrop-blur-sm border-b border-gray-200 mb-8">
        <div className="max-w-7xl mx-auto px-4 overflow-x-auto">
          <div className="flex space-x-8 py-4">
            {categories.map((cat) => (
              <a key={cat.id} href={`#${cat.id}`} className="text-gray-600 hover:text-primary font-medium whitespace-nowrap">
                {cat.name}
              </a>
            ))}
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4">
        <h2 id="pizza" className="text-3xl font-bold mb-8 text-gray-900">Pizza</h2>
        {loading ? (
          <div className="text-center py-20">Loading delicious pizzas...</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
            {pizzas.filter(p => p.category === 'pizza').map((pizza) => (
              <ProductCard key={pizza.id} pizza={pizza} />
            ))}
          </div>
        )}

        <h2 id="drinks" className="text-3xl font-bold mt-16 mb-8 text-gray-900">Drinks</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
          {pizzas.filter(p => p.category === 'drinks').map((pizza) => (
            <ProductCard key={pizza.id} pizza={pizza} />
          ))}
        </div>
        {pizzas.filter(p => p.category === 'drinks').length === 0 && !loading && <div className="text-gray-500">No drinks available.</div>}

        <h2 id="desserts" className="text-3xl font-bold mt-16 mb-8 text-gray-900">Desserts</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
          {pizzas.filter(p => p.category === 'desserts').map((pizza) => (
            <ProductCard key={pizza.id} pizza={pizza} />
          ))}
        </div>
        {pizzas.filter(p => p.category === 'desserts').length === 0 && !loading && <div className="text-gray-500">No desserts available.</div>}
      </div>
    </section>
  );
};