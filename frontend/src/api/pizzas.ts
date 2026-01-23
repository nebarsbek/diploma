import { api } from './client';
import type { Pizza, CreatePizzaData } from '../types';

export const getPizzas = async (category?: string): Promise<Pizza[]> => {
  const response = await api.get<Pizza[]>('/pizzas/', {
    params: category ? { category } : {}
  });
  return response.data;
};

export const searchPizzas = async (query: string): Promise<Pizza[]> => {
  const response = await api.get<Pizza[]>('/pizzas/search', {
    params: { query }
  });
  return response.data;
};

export const createPizza = async (data: CreatePizzaData): Promise<Pizza> => {
  const response = await api.post<Pizza>('/pizzas/', data);
  return response.data;
};

export const updatePizza = async (id: number, data: CreatePizzaData): Promise<Pizza> => {
  const response = await api.put<Pizza>(`/pizzas/${id}`, data);
  return response.data;
};

export const deletePizza = async (id: number): Promise<void> => {
  await api.delete(`/pizzas/${id}`);
};
