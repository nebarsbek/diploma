import { motion } from 'framer-motion';

export const Hero = () => {
  return (
    <section className="relative h-[60vh] flex items-center justify-center overflow-hidden bg-gray-900">
      <div className="absolute inset-0 z-0">
        <img 
          src="https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&q=80&w=2070" 
          alt="Pizza Background" 
          className="w-full h-full object-cover opacity-40"
        />
      </div>
      
      <div className="relative z-10 text-center text-white px-4">
        <motion.h1 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-5xl md:text-7xl font-bold mb-6"
        >
          Authentic Italian <span className="text-primary">Taste</span>
        </motion.h1>
        <motion.p 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="text-xl md:text-2xl text-gray-200 mb-8 max-w-2xl mx-auto"
        >
          Handcrafted pizzas delivered straight to your doorstep.
        </motion.p>
        <motion.a
          href="#menu"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.4 }}
          className="inline-block bg-primary hover:bg-orange-700 text-white font-bold py-3 px-8 rounded-full text-lg transition-colors"
        >
          Order Now
        </motion.a>
      </div>
    </section>
  );
};