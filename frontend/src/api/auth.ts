import { api } from './client';
import type { Token, User } from '../types';

export const login = async (username: string, password: string): Promise<Token> => {
  const response = await api.post<Token>('/auth/login', {
    email: username,
    password,
  });
  return response.data;
};

export const register = async (username: string, password: string): Promise<void> => {
  await api.post('/auth/register', {
    email: username,
    password,
  });
};

export const getMe = async (): Promise<User> => {
  const response = await api.get<User>('/auth/me');
  return response.data;
};

export const changePassword = async (oldPassword: string, newPassword: string): Promise<void> => {
  await api.post('/auth/change-password', {
    old_password: oldPassword,
    new_password: newPassword,
  });
};

export const forgotPassword = async (email: string): Promise<void> => {
  await api.post('/auth/forgot-password', { email });
};

export const resetPassword = async (token: string, newPassword: string): Promise<void> => {
  await api.post('/auth/reset-password', { token, new_password: newPassword });
};
