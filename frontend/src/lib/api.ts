import axios from 'axios';

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use((config) => {
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('token');
      }
    }
    return Promise.reject(error);
  }
);

export interface Article {
  id: number;
  title: string;
  title_zh?: string;
  url: string;
  summary?: string;
  summary_zh?: string;
  source: string;
  category: string;
  authors: string[];
  tags: string[];
  quality_score: number;
  published_at?: string;
  crawled_at: string;
}

export interface ArticleListResponse {
  total: number;
  page: number;
  page_size: number;
  items: Article[];
}

export interface ArticleFilters {
  page?: number;
  page_size?: number;
  category?: string;
  source?: string;
  min_score?: number;
  search?: string;
}

// Articles API
export const articlesApi = {
  getArticles: async (filters: ArticleFilters = {}): Promise<ArticleListResponse> => {
    const params = new URLSearchParams();
    if (filters.page) params.append('page', filters.page.toString());
    if (filters.page_size) params.append('page_size', filters.page_size.toString());
    if (filters.category) params.append('category', filters.category);
    if (filters.source) params.append('source', filters.source);
    if (filters.min_score) params.append('min_score', filters.min_score.toString());
    if (filters.search) params.append('search', filters.search);
    
    const response = await api.get(`/articles?${params.toString()}`);
    return response.data;
  },
  
  getTodayArticles: async (limit: number = 10, minScore: number = 60): Promise<Article[]> => {
    const response = await api.get(`/articles/today?limit=${limit}&min_score=${minScore}`);
    return response.data;
  },
  
  getArticle: async (id: number): Promise<Article> => {
    const response = await api.get(`/articles/${id}`);
    return response.data;
  },
  
  getCategories: async () => {
    const response = await api.get('/articles/categories');
    return response.data;
  },
  
  getSources: async () => {
    const response = await api.get('/articles/sources');
    return response.data;
  },
};

// Users API
export const usersApi = {
  register: async (email: string, password: string, username?: string) => {
    const response = await api.post('/users/register', { email, password, username });
    return response.data;
  },
  
  login: async (email: string, password: string) => {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);
    
    const response = await api.post('/users/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
    return response.data;
  },
  
  getMe: async () => {
    const response = await api.get('/users/me');
    return response.data;
  },
  
  updateMe: async (data: Record<string, unknown>) => {
    const response = await api.put('/users/me', data);
    return response.data;
  },
};

// Admin API
export const adminApi = {
  triggerCrawl: async () => {
    const response = await api.post('/admin/crawl');
    return response.data;
  },
  
  triggerProcess: async (limit: number = 20) => {
    const response = await api.post(`/admin/process?limit=${limit}`);
    return response.data;
  },
  
  getStats: async () => {
    const response = await api.get('/admin/stats');
    return response.data;
  },
};

export default api;
