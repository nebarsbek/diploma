import { api } from './client';
import type { CreateOrderData, Order, OrderStatusUpdateData } from '../types';

export const createOrder = async (data: CreateOrderData): Promise<void> => {
  await api.post('/orders/create', data);
};

export const getOrders = async (): Promise<Order[]> => {
  // Примечание: этот эндпоинт в текущей реализации бэкенда возвращает заказы только для текущего пользователя.
  // Чтобы администратор видел все заказы, требуется доработка бэкенда.
  const response = await api.get<Order[]>('/orders/');
  return response.data;
};

export const updateOrderStatus = async (orderId: number, data: OrderStatusUpdateData): Promise<Order> => {
  const response = await api.patch<Order>(`/orders/${orderId}/status`, data);
  return response.data;
};