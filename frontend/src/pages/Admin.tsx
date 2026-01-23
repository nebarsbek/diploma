import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api/client';
import { getPizzas, createPizza, updatePizza, deletePizza } from '../api/pizzas';
import { getOrders, updateOrderStatus } from '../api/orders';
import type { Pizza, CreatePizzaData, Order } from '../types';
import { Trash2, Edit, Plus, LogOut, X, UserPlus } from 'lucide-react';
import { useAuth } from '../context/useAuth';

export const Admin = () => {
  const { user, logout, isLoading } = useAuth();
  const navigate = useNavigate();

  const [selectedTab, setSelectedTab] = useState<'products' | 'orders'>('products');
  const activeTab = user?.role === 'employee' ? 'orders' : selectedTab;

  const [pizzas, setPizzas] = useState<Pizza[]>([]);
  const [orders, setOrders] = useState<Order[]>([]);

  const [isEditing, setIsEditing] = useState<Pizza | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isUserModalOpen, setIsUserModalOpen] = useState(false);
  const [newUserEmail, setNewUserEmail] = useState('');
  const [newUserPassword, setNewUserPassword] = useState('');
  const [orderStatusFilter, setOrderStatusFilter] = useState('all');
  const [selectedCategory, setSelectedCategory] = useState('all');
  
  const [formData, setFormData] = useState<Omit<CreatePizzaData, 'price'> & { price: string | number }>({
    name: '',
    price: 0,
    description: '',
    image_url: '',
    category: 'pizza'
  });

  const fetchPizzas = useCallback(async () => {
    try {
      const category = selectedCategory === 'all' ? undefined : selectedCategory;
      const data = await getPizzas(category);
      setPizzas(data);
    } catch (error) {
      console.error('Failed to fetch pizzas', error);
    }
  }, [selectedCategory]);

  const fetchOrders = useCallback(async () => {
    try {
      const data = await getOrders();
      setOrders(data);
    } catch (error) {
      console.error('Failed to fetch orders', error);
    }
  }, []);

  useEffect(() => {
    if (!isLoading && !user) {
      navigate('/login');
      return;
    }

    if (user) {
      const loadData = async () => {
        if (activeTab === 'products' && user.role === 'admin') {
          await fetchPizzas();
        } else {
          await fetchOrders();
        }
      };
      loadData();
    }
  }, [user, isLoading, activeTab, fetchPizzas, fetchOrders, navigate]);

  const handleStatusChange = async (orderId: number, status: string) => {
    try {
      await updateOrderStatus(orderId, { status });
      fetchOrders(); // refetch orders to show update
    } catch (error) {
      console.error('Failed to update order status', error);
      alert('Failed to update order status');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const submissionData = { ...formData, price: Number(formData.price) };
      if (isEditing) {
        await updatePizza(isEditing.id, submissionData);
      } else {
        await createPizza(submissionData);
      }
      setIsModalOpen(false);
      setIsEditing(null);
      setFormData({ name: '', price: 0, description: '', image_url: '', category: 'pizza' });
      fetchPizzas();
    } catch (error) {
      console.error('Operation failed', error);
      alert('Failed to save pizza');
    }
  };

  const handleCreateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
        await api.post('/auth/create-user', { email: newUserEmail, password: newUserPassword });
        setIsUserModalOpen(false);
        setNewUserEmail('');
        setNewUserPassword('');
        alert('User created successfully');
    } catch (e) {
        alert('Failed to create user');
        console.log(e);
    }
  };

  const handleDelete = async (id: number) => {
    if (confirm('Are you sure?')) {
      try {
        await deletePizza(id);
        fetchPizzas();
      } catch (error) {
        console.error('Delete failed', error);
      }
    }
  };

  const openModal = (pizza?: Pizza) => {
    if (pizza) {
      setIsEditing(pizza);
      setFormData({
        name: pizza.name,
        price: pizza.price,
        description: pizza.description,
        image_url: pizza.image_url || '',
        category: pizza.category || 'pizza'
      });
    } else {
      setIsEditing(null);
      setFormData({ name: '', price: 0, description: '', image_url: '', category: 'pizza' });
    }
    setIsModalOpen(true);
  };

  if (isLoading || !user) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
  }

  if (!['admin', 'employee'].includes(user.role)) {
    return <div className="min-h-screen flex items-center justify-center">Access Denied</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">Admin Panel</h1>
          <div className="flex gap-4">
            {activeTab === 'products' && user.role === 'admin' && (
              <button onClick={() => openModal()} className="flex items-center gap-2 bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
                <Plus size={20} /> Add Product
              </button>
            )}
            {user.role === 'admin' && (
                <button onClick={() => setIsUserModalOpen(true)} className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
                    <UserPlus size={20} /> Add Employee
                </button>
            )}
            <button onClick={logout} className="flex items-center gap-2 bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700">
              <LogOut size={20} /> Logout
            </button>
          </div>
        </div>

        {/* Tabs */}
        <div className="border-b border-gray-200 mb-8">
          <nav className="-mb-px flex space-x-8" aria-label="Tabs">
            <button
              onClick={() => user.role === 'admin' && setSelectedTab('products')}
              disabled={user.role !== 'admin'}
              className={`${
                activeTab === 'products'
                  ? 'border-primary text-primary'
                  : user.role === 'admin' ? 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300' : 'text-gray-300 cursor-not-allowed'
              } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
            >
              Product Management
            </button>
            <button
              onClick={() => setSelectedTab('orders')}
              className={`${
                activeTab === 'orders'
                  ? 'border-primary text-primary'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
            >
              Order Management
            </button>
          </nav>
        </div>

        {activeTab === 'products' && user.role === 'admin' && (
          <>
            <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
              {['all', 'pizza', 'drinks', 'desserts'].map(cat => (
                <button
                  key={cat}
                  onClick={() => setSelectedCategory(cat)}
                  className={`px-4 py-2 rounded-full capitalize whitespace-nowrap transition-colors ${
                    selectedCategory === cat
                      ? 'bg-primary text-white'
                      : 'bg-white text-gray-600 hover:bg-gray-100 border border-gray-200'
                  }`}
                >
                  {cat}
                </button>
              ))}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {pizzas.map(pizza => (
                <div key={pizza.id} className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 flex flex-col">
                  <img src={pizza.image_url || 'https://placehold.co/600x400'} alt={pizza.name} className="w-full h-48 object-cover rounded-lg mb-4" />
                  <h3 className="text-xl font-bold mb-2">{pizza.name}</h3>
                  <p className="text-gray-500 text-sm mb-4 flex-grow">{pizza.description}</p>
                  <div className="flex justify-between items-center mt-auto">
                    <span className="text-xl font-bold text-primary">${Number(pizza.price).toFixed(2)}</span>
                    <div className="flex gap-2">
                      <button onClick={() => openModal(pizza)} className="p-2 text-blue-600 hover:bg-blue-50 rounded"><Edit size={20} /></button>
                      <button onClick={() => handleDelete(pizza.id)} className="p-2 text-red-600 hover:bg-red-50 rounded"><Trash2 size={20} /></button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}

        {activeTab === 'orders' && (
          <div>
            <div className="mb-4">
                <select 
                    value={orderStatusFilter} 
                    onChange={(e) => setOrderStatusFilter(e.target.value)}
                    className="p-2 border rounded"
                >
                    <option value="all">All Statuses</option>
                    <option value="pending">Pending</option>
                    <option value="processing">Processing</option>
                    <option value="delivered">Delivered</option>
                    <option value="cancelled">Cancelled</option>
                </select>
            </div>
            <div className="bg-white shadow-sm rounded-xl overflow-x-auto">
              <table className="w-full text-sm text-left text-gray-500">
                <thead className="text-xs text-gray-700 uppercase bg-gray-50">
                  <tr>
                    <th scope="col" className="px-6 py-3">Order ID</th>
                    <th scope="col" className="px-6 py-3">User ID</th>
                    <th scope="col" className="px-6 py-3">Total Price</th>
                    <th scope="col" className="px-6 py-3">Status</th>
                    <th scope="col" className="px-6 py-3">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {orders
                    .filter(o => orderStatusFilter === 'all' || o.status === orderStatusFilter)
                    .map(order => (
                    <tr key={order.id} className="bg-white border-b hover:bg-gray-50">
                      <th scope="row" className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap">
                        #{order.id}
                      </th>
                      <td className="px-6 py-4">{order.user_id}</td>
                      <td className="px-6 py-4">${Number(order.total_price).toFixed(2)}</td>
                      <td className="px-6 py-4 capitalize">{order.status}</td>
                      <td className="px-6 py-4">
                        <select
                          disabled={user.role !== 'admin'}
                          value={order.status}
                          onChange={(e) => handleStatusChange(order.id, e.target.value)}
                          className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary focus:border-primary block w-full p-2"
                        >
                          <option value="pending">Pending</option>
                          <option value="processing">Processing</option>
                          <option value="delivered">Delivered</option>
                          <option value="cancelled">Cancelled</option>
                        </select>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {isModalOpen && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
            <div className="bg-white p-8 rounded-xl w-full max-w-md relative">
              <button onClick={() => setIsModalOpen(false)} className="absolute top-4 right-4 text-gray-500 hover:text-gray-700"><X /></button>
              <h2 className="text-2xl font-bold mb-6">{isEditing ? 'Edit Pizza' : 'Add New Pizza'}</h2>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
                  <input type="text" required className="w-full p-2 border rounded" value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Price</label>
                  <input type="number" step="0.01" required className="w-full p-2 border rounded" value={formData.price} onChange={e => setFormData({...formData, price: e.target.value})} />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
                  <select className="w-full p-2 border rounded" value={formData.category} onChange={e => setFormData({...formData, category: e.target.value as 'pizza' | 'drinks' | 'desserts'})}>
                    <option value="pizza">Pizza</option>
                    <option value="drinks">Drinks</option>
                    <option value="desserts">Desserts</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                  <textarea required className="w-full p-2 border rounded" rows={3} value={formData.description} onChange={e => setFormData({...formData, description: e.target.value})} />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Image URL</label>
                  <input type="text" className="w-full p-2 border rounded" value={formData.image_url} onChange={e => setFormData({...formData, image_url: e.target.value})} />
                </div>
                <button type="submit" className="w-full bg-primary text-white py-2 rounded font-bold hover:bg-orange-700 mt-4">
                  {isEditing ? 'Update' : 'Create'}
                </button>
              </form>
            </div>
          </div>
        )}

        {isUserModalOpen && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
            <div className="bg-white p-8 rounded-xl w-full max-w-md relative">
              <button onClick={() => setIsUserModalOpen(false)} className="absolute top-4 right-4 text-gray-500 hover:text-gray-700"><X /></button>
              <h2 className="text-2xl font-bold mb-6">Add Employee</h2>
              <form onSubmit={handleCreateUser} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                  <input type="email" required className="w-full p-2 border rounded" value={newUserEmail} onChange={e => setNewUserEmail(e.target.value)} />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
                  <input type="password" required className="w-full p-2 border rounded" value={newUserPassword} onChange={e => setNewUserPassword(e.target.value)} />
                </div>
                <button type="submit" className="w-full bg-primary text-white py-2 rounded font-bold hover:bg-orange-700 mt-4">
                  Create Employee
                </button>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};