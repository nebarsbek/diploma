export interface Pizza {
  id: number;
  name: string;
  price: number;
  description: string;
  image_url: string | null;
  category: 'pizza' | 'drinks' | 'desserts';
}

export interface CartItem extends Pizza {
  cartId: string;
  quantity: number;
  selectedSize: '30cm' | '40cm';
}

export interface CreateOrderItemData {
  product_id: number;
  quantity: number;
}

export interface CreateOrderData {
  items: CreateOrderItemData[];
  delivery_address: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface CreatePizzaData {
  name: string;
  price: number;
  description: string;
  image_url: string;
  category: 'pizza' | 'drinks' | 'desserts';
}

export interface OrderItem {
  product_id: number;
  price: number;
  quantity: number;
}

export interface Order {
  id: number;
  user_id: number;
  status: string;
  delivery_address: string;
  items: OrderItem[];
  total_price: number;
}

export interface OrderStatusUpdateData {
  status: string;
}

export interface User {
  id: number;
  email: string;
  role: string;
}

