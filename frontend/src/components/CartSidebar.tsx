import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Minus, Plus, Trash2, CreditCard, Banknote } from 'lucide-react';
import { useCart } from '../context/CartContext';

export const CartSidebar = () => {
  const { isOpen, toggleCart, items, updateQuantity, removeFromCart, totalPrice, checkout } = useCart();
  const [address, setAddress] = useState('');
  const [paymentMethod, setPaymentMethod] = useState<'cash' | 'card'>('cash');

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={toggleCart}
            className="fixed inset-0 bg-black/50 z-50 backdrop-blur-sm"
          />
          
          {/* Sidebar */}
          <motion.div
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
            className="fixed right-0 top-0 h-full w-full max-w-md bg-white z-50 shadow-2xl flex flex-col"
          >
            <div className="p-6 border-b flex items-center justify-between bg-gray-50">
              <h2 className="text-2xl font-bold text-gray-900">Your Order</h2>
              <button onClick={toggleCart} className="p-2 hover:bg-gray-200 rounded-full transition-colors">
                <X size={24} />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-6 space-y-6">
              {items.length === 0 ? (
                <div className="text-center text-gray-500 mt-10">Your cart is empty 😔</div>
              ) : (
                items.map((item) => (
                  <div key={item.cartId} className="flex gap-4 bg-white p-4 rounded-xl border border-gray-100 shadow-sm">
                    <div className="flex-1">
                      <h4 className="font-bold text-gray-900">{item.name}</h4>
                      <p className="text-sm text-gray-500 mb-2">Size: {item.selectedSize}</p>
                      <div className="flex items-center gap-3">
                        <button onClick={() => updateQuantity(item.cartId, -1)} className="p-1 bg-gray-100 rounded hover:bg-gray-200"><Minus size={16} /></button>
                        <span className="font-medium w-6 text-center">{item.quantity}</span>
                        <button onClick={() => updateQuantity(item.cartId, 1)} className="p-1 bg-gray-100 rounded hover:bg-gray-200"><Plus size={16} /></button>
                      </div>
                    </div>
                    <div className="flex flex-col items-end justify-between">
                      <span className="font-bold text-lg">${(Number(item.price) * item.quantity).toFixed(2)}</span>
                      <button onClick={() => removeFromCart(item.cartId)} className="text-red-500 hover:text-red-700"><Trash2 size={18} /></button>
                    </div>
                  </div>
                ))
              )}
            </div>

            <div className="p-6 border-t bg-gray-50">
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">Delivery Address</label>
                <textarea
                  value={address}
                  onChange={(e) => setAddress(e.target.value)}
                  placeholder="Enter your delivery address..."
                  className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent outline-none text-sm resize-none"
                  rows={3}
                />
              </div>

              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">Payment Method</label>
                <div className="grid grid-cols-2 gap-3">
                  <button
                    onClick={() => setPaymentMethod('cash')}
                    className={`flex items-center justify-center gap-2 p-3 rounded-xl border transition-all ${
                      paymentMethod === 'cash'
                        ? 'border-primary bg-orange-50 text-primary shadow-sm'
                        : 'border-gray-200 text-gray-600 hover:border-primary/50'
                    }`}
                  >
                    <Banknote size={20} />
                    <span className="font-medium">Cash</span>
                  </button>
                  
                  <button
                    disabled
                    className="flex items-center justify-center gap-2 p-3 rounded-xl border border-gray-100 bg-gray-50 text-gray-400 cursor-not-allowed relative overflow-hidden"
                  >
                    <CreditCard size={20} />
                    <span className="font-medium">Card</span>
                    <div className="absolute top-0 right-0 bg-gray-200 text-[10px] font-bold px-1.5 py-0.5 rounded-bl-lg text-gray-500">
                      SOON
                    </div>
                  </button>
                </div>
              </div>

              <div className="flex justify-between items-center mb-6">
                <span className="text-lg font-medium text-gray-600">Total:</span>
                <span className="text-3xl font-bold text-primary">${totalPrice.toFixed(2)}</span>
              </div>
              <button 
                onClick={() => checkout(address)}
                disabled={items.length === 0 || !address.trim()}
                className="w-full bg-primary hover:bg-orange-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-bold py-4 rounded-xl text-lg transition-colors shadow-lg shadow-orange-200"
              >
                Checkout
              </button>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};