/**
 * Store Zustand pour la gestion de l'état de l'application
 * Optimisation de Portefeuille - Markowitz
 */

import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import * as SecureStore from 'expo-secure-store';
import type {
  AuthState,
  User,
  Portfolio,
  Asset,
  InvestmentStrategy,
  EfficientFrontier,
  OptimizationConstraints,
} from '@/types/portfolio';

// === Storage sécurisé pour Expo ===
const secureStorage = {
  getItem: async (name: string): Promise<string | null> => {
    return await SecureStore.getItemAsync(name);
  },
  setItem: async (name: string, value: string): Promise<void> => {
    await SecureStore.setItemAsync(name, value);
  },
  removeItem: async (name: string): Promise<void> => {
    await SecureStore.deleteItemAsync(name);
  },
};

// === Auth Store ===
interface AuthStore extends AuthState {
  login: (user: User, token: string) => void;
  logout: () => void;
  setLoading: (loading: boolean) => void;
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,

      login: (user, token) =>
        set({ user, token, isAuthenticated: true, isLoading: false }),

      logout: () =>
        set({ user: null, token: null, isAuthenticated: false, isLoading: false }),

      setLoading: (isLoading) => set({ isLoading }),
    }),
    {
      name: 'auth-storage',
      storage: createJSONStorage(() => secureStorage),
    }
  )
);

// === Portfolio Store ===
interface PortfolioState {
  portfolios: Portfolio[];
  currentPortfolio: Portfolio | null;
  assets: Asset[];
  isLoading: boolean;
  error: string | null;
}

interface PortfolioActions {
  setPortfolios: (portfolios: Portfolio[]) => void;
  addPortfolio: (portfolio: Portfolio) => void;
  updatePortfolio: (id: string, updates: Partial<Portfolio>) => void;
  deletePortfolio: (id: string) => void;
  setCurrentPortfolio: (portfolio: Portfolio | null) => void;
  setAssets: (assets: Asset[]) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  reset: () => void;
}

const initialPortfolioState: PortfolioState = {
  portfolios: [],
  currentPortfolio: null,
  assets: [],
  isLoading: false,
  error: null,
};

export const usePortfolioStore = create<PortfolioState & PortfolioActions>()(
  (set) => ({
    ...initialPortfolioState,

    setPortfolios: (portfolios) => set({ portfolios }),

    addPortfolio: (portfolio) =>
      set((state) => ({ portfolios: [...state.portfolios, portfolio] })),

    updatePortfolio: (id, updates) =>
      set((state) => ({
        portfolios: state.portfolios.map((p) =>
          p.id === id ? { ...p, ...updates } : p
        ),
      })),

    deletePortfolio: (id) =>
      set((state) => ({
        portfolios: state.portfolios.filter((p) => p.id !== id),
      })),

    setCurrentPortfolio: (currentPortfolio) => set({ currentPortfolio }),

    setAssets: (assets) => set({ assets }),

    setLoading: (isLoading) => set({ isLoading }),

    setError: (error) => set({ error }),

    reset: () => set(initialPortfolioState),
  })
);

// === Optimization Store ===
interface OptimizationState {
  constraints: OptimizationConstraints;
  frontier: EfficientFrontier | null;
  selectedPoint: number | null; // Index du point sélectionné sur la frontière
  isOptimizing: boolean;
}

interface OptimizationActions {
  setConstraints: (constraints: Partial<OptimizationConstraints>) => void;
  setFrontier: (frontier: EfficientFrontier | null) => void;
  selectPoint: (index: number | null) => void;
  setOptimizing: (optimizing: boolean) => void;
  resetOptimization: () => void;
}

const defaultConstraints: OptimizationConstraints = {
  targetReturn: undefined,
  maxVolatility: undefined,
  minWeight: 0,
  maxWeight: 1,
  allowShortSelling: false,
  riskFreeRate: 0.02, // 2% par défaut
};

export const useOptimizationStore = create<OptimizationState & OptimizationActions>()(
  (set) => ({
    constraints: defaultConstraints,
    frontier: null,
    selectedPoint: null,
    isOptimizing: false,

    setConstraints: (newConstraints) =>
      set((state) => ({
        constraints: { ...state.constraints, ...newConstraints },
      })),

    setFrontier: (frontier) => set({ frontier }),

    selectPoint: (selectedPoint) => set({ selectedPoint }),

    setOptimizing: (isOptimizing) => set({ isOptimizing }),

    resetOptimization: () =>
      set({
        constraints: defaultConstraints,
        frontier: null,
        selectedPoint: null,
        isOptimizing: false,
      }),
  })
);

// === Strategy Store ===
interface StrategyState {
  strategies: InvestmentStrategy[];
  activeStrategy: InvestmentStrategy | null;
}

interface StrategyActions {
  setStrategies: (strategies: InvestmentStrategy[]) => void;
  addStrategy: (strategy: InvestmentStrategy) => void;
  setActiveStrategy: (strategy: InvestmentStrategy | null) => void;
  removeStrategy: (id: string) => void;
}

export const useStrategyStore = create<StrategyState & StrategyActions>()(
  (set) => ({
    strategies: [],
    activeStrategy: null,

    setStrategies: (strategies) => set({ strategies }),

    addStrategy: (strategy) =>
      set((state) => ({ strategies: [...state.strategies, strategy] })),

    setActiveStrategy: (activeStrategy) => set({ activeStrategy }),

    removeStrategy: (id) =>
      set((state) => ({
        strategies: state.strategies.filter((s) => s.id !== id),
      })),
  })
);
