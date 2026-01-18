import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
  id: number;
  email: string;
  username?: string;
  preferred_categories: string[];
  preferred_sources: string[];
  min_quality_score: number;
  email_frequency: string;
  email_enabled: boolean;
}

interface AppState {
  user: User | null;
  token: string | null;
  filters: {
    category: string;
    source: string;
    minScore: number;
    search: string;
  };
  setUser: (user: User | null) => void;
  setToken: (token: string | null) => void;
  setFilters: (filters: Partial<AppState['filters']>) => void;
  logout: () => void;
}

export const useStore = create<AppState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      filters: {
        category: '',
        source: '',
        minScore: 0,
        search: '',
      },
      setUser: (user) => set({ user }),
      setToken: (token) => {
        if (token) {
          localStorage.setItem('token', token);
        } else {
          localStorage.removeItem('token');
        }
        set({ token });
      },
      setFilters: (filters) =>
        set((state) => ({
          filters: { ...state.filters, ...filters },
        })),
      logout: () => {
        localStorage.removeItem('token');
        set({ user: null, token: null });
      },
    }),
    {
      name: 'ai-news-storage',
      partialize: (state) => ({
        token: state.token,
        filters: state.filters,
      }),
    }
  )
);
