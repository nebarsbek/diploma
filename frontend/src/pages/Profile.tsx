import { useEffect, useState } from 'react';
import { getOrders } from '../api/orders';
import { getPizzas } from '../api/pizzas';
import type { Order } from '../types';
import { useAuth } from '../context/useAuth';
import { Navbar } from '../components/Navbar';
import { CartSidebar } from '../components/CartSidebar';

export const Profile = () => {
  const { user } = useAuth();
  const [orders, setOrders] = useState<Order[]>([]);
  const [productNames, setProductNames] = useState<Record<number, string>>({});
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [ordersData, pizzasData] = await Promise.all([
          getOrders(),
          getPizzas()
        ]);
        setOrders(ordersData);
        
        const names: Record<number, string> = {};
        pizzasData.forEach(p => names[p.id] = p.name);
        setProductNames(names);
      } catch (error) {
        console.error('Failed to fetch data', error);
      } finally {
        setLoading(false);
      }
    };
    if (user) {
        loadData();
    }
  }, [user]);

  const filteredOrders = statusFilter === 'all' 
    ? orders 
    : orders.filter(order => order.status === statusFilter);

  if (!user) return null;

  return (
    <div className="min-h-screen bg-gray-50 pt-24 pb-12 px-4">
      <Navbar />
      <CartSidebar />
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">My Profile</h1>
        
        <div className="bg-white rounded-xl shadow-sm p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Account Details</h2>
          <div className="space-y-2">
            <p className="text-gray-600">Email: <span className="text-gray-900 font-medium">{user.email}</span></p>
            <p className="text-gray-600">Role: <span className="text-gray-900 font-medium capitalize">{user.role}</span></p>
          </div>
        </div>

        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold">Order History</h2>
          <select 
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="p-2 border rounded-lg bg-white shadow-sm"
          >
            <option value="all">All Statuses</option>
            <option value="pending">Pending</option>
            <option value="processing">Processing</option>
           <option value="delivered">Delivered</option>
            <option value="cancelled">Cancelled</option>
          </select>
        </div>

        {loading ? (
          <div className="text-center py-8">Loading orders...</div>
        ) : filteredOrders.length === 0 ? (
          <div className="bg-white rounded-xl shadow-sm p-8 text-center text-gray-500">
            No orders found.
          </div>
        ) : (
          <div className="space-y-4">
            {filteredOrders.map((order) => (
              <div key={order.id} className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
                <div className="flex flex-wrap justify-between items-start mb-4 gap-4">
                  <div>
                    <span className="font-bold text-lg mr-3">Order #{order.id}</span>
                    <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide ${
                      order.status === 'delivered' ? 'bg-green-100 text-green-800' :
                      order.status === 'cancelled' ? 'bg-red-100 text-red-800' :
                      'bg-blue-100 text-blue-800'
                    }`}>
                      {order.status}
                    </span>
                  </div>
                  <span className="font-bold text-primary text-xl">${Number(order.total_price).toFixed(2)}</span>
                </div>
                
                <div className="text-sm text-gray-600 mb-4 bg-gray-50 p-3 rounded-lg">
                  <span className="font-medium">Delivery Address:</span> {order.delivery_address}
               </div>
                
                <div className="border-t pt-4">
                  <h4 className="font-medium mb-3 text-sm text-gray-500 uppercase tracking-wider">Items</h4>
                  <ul className="space-y-2">
                    {order.items.map((item, index) => (
                      <li key={index} className="flex justify-between text-sm items-center">
                        <span className="font-medium">
                          {productNames[item.product_id] || `Product #${item.product_id}`} 
                          <span className="text-gray-500 ml-2">x{item.quantity}</span>
                        </span>
                        <span className="text-gray-600">${Number(item.price).toFixed(2)}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
