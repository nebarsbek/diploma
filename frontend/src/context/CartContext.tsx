import { createContext, useContext, useState, type ReactNode } from 'react';
import type { Pizza, CartItem, CreateOrderData } from '../types';
import { createOrder } from '../api/orders';

interface CartContextType {
  items: CartItem[];
  isOpen: boolean;
  addToCart: (pizza: Pizza, size: '30cm' | '40cm') => void;
  removeFromCart: (cartId: string) => void;
  updateQuantity: (cartId: string, delta: number) => void;
  toggleCart: () => void;
  checkout: (address: string) => Promise<void>;
  totalPrice: number;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

export const CartProvider = ({ children }: { children: ReactNode }) => {
  const [items, setItems] = useState<CartItem[]>([]);
  const [isOpen, setIsOpen] = useState(false);

  const addToCart = (pizza: Pizza, size: '30cm' | '40cm') => {
    const priceMultiplier = size === '40cm' ? 1.3 : 1;
    const newItem: CartItem = {
      ...pizza,
      price: Number(pizza.price) * priceMultiplier,
      cartId: `${pizza.id}-${size}-${Date.now()}`,
      quantity: 1,
      selectedSize: size,
    };
    setItems(prev => [...prev, newItem]);
    setIsOpen(true);
  };

  const removeFromCart = (cartId: string) => {
    setItems(prev => prev.filter(item => item.cartId !== cartId));
  };

  const updateQuantity = (cartId: string, delta: number) => {
    setItems(prev => prev.map(item => {
      if (item.cartId === cartId) {
        const newQuantity = item.quantity + delta;
        return newQuantity > 0 ? { ...item, quantity: newQuantity } : item;
      }
      return item;
    }));
  };

  const toggleCart = () => setIsOpen(!isOpen);

  const totalPrice = items.reduce((sum, item) => sum + (Number(item.price) * item.quantity), 0);

  const checkout = async (address: string) => {
    if (items.length === 0) return;

    const orderData: CreateOrderData = {
      items: items.map(item => ({
        product_id: item.id,
        quantity: item.quantity
      })),
      delivery_address: address
    };

    try {
      await createOrder(orderData);
      setItems([]);
      setIsOpen(false);
      alert('Order placed successfully!');
    } catch (error) {
      console.error('Checkout failed:', error);
      alert('Failed to place order.');
    }
  };

  return (
    <CartContext.Provider value={{ items, isOpen, addToCart, removeFromCart, updateQuantity, toggleCart, totalPrice, checkout }}>
      {children}
    </CartContext.Provider>
  );
};

// eslint-disable-next-line react-refresh/only-export-components
export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) throw new Error('useCart must be used within a CartProvider');
  return context;
};