/**
 * Types pour l'optimisation de portefeuille - Modèle Markowitz
 * Basé sur les 14 points du document prog_finance_fr_v2
 */

// === Actifs et Données de Marché ===

export interface Asset {
  id: string;
  symbol: string;
  name: string;
  sector?: string;
  currency: string;
}

export interface AssetReturns {
  assetId: string;
  returns: number[];        // Rendements historiques
  dates: string[];          // Dates correspondantes
  expectedReturn: number;   // Espérance μ
  volatility: number;       // Écart-type σ
}

// === Matrice de Covariance ===

export interface CovarianceMatrix {
  assetIds: string[];
  matrix: number[][];       // Σ - matrice de covariance
  correlationMatrix: number[][];  // Matrice de corrélation ρ
}

// === Portefeuille ===

export interface PortfolioWeights {
  weights: Record<string, number>;  // w_i pour chaque actif
  sumWeights: number;               // Σw_i (doit être = 1)
}

export interface PortfolioMetrics {
  expectedReturn: number;   // μ_p = w'μ
  variance: number;         // σ²_p = w'Σw
  volatility: number;       // σ_p = √(w'Σw)
  sharpeRatio: number;      // (μ_p - r_f) / σ_p
}

export interface Portfolio {
  id: string;
  name: string;
  weights: PortfolioWeights;
  metrics: PortfolioMetrics;
  createdAt: string;
  updatedAt: string;
}

// === Contraintes d'Optimisation ===

export interface OptimizationConstraints {
  targetReturn?: number;           // r* - rendement cible
  maxVolatility?: number;          // σ_max - risque maximum toléré
  minWeight?: number;              // w_min - poids minimum par actif (défaut 0)
  maxWeight?: number;              // w_max - poids maximum par actif (défaut 1)
  allowShortSelling: boolean;      // Autoriser les ventes à découvert
  riskFreeRate: number;            // r_f - taux sans risque
}

// === Frontière Efficiente ===

export interface EfficientFrontierPoint {
  targetReturn: number;     // r*
  portfolioReturn: number;  // μ_p effectif
  portfolioRisk: number;    // σ_p
  weights: number[];        // Allocations optimales
  sharpeRatio: number;
}

export interface EfficientFrontier {
  points: EfficientFrontierPoint[];
  minVariancePortfolio: EfficientFrontierPoint;
  maxSharpePortfolio: EfficientFrontierPoint;  // Portefeuille tangent
}

// === Copules (Point 5 du document) ===

export type CopulaType = 'gaussian' | 'student-t' | 'clayton' | 'gumbel' | 'frank';

export interface CopulaParams {
  type: CopulaType;
  correlation?: number;     // Pour Gaussienne
  degreesOfFreedom?: number; // Pour Student-t
  theta?: number;           // Paramètre de dépendance
}

// === Stratégie d'Investissement ===

export interface InvestmentStrategy {
  id: string;
  name: string;
  description: string;
  constraints: OptimizationConstraints;
  rebalancingFrequency: 'daily' | 'weekly' | 'monthly' | 'quarterly';
  riskProfile: 'conservative' | 'moderate' | 'aggressive';
  createdAt: string;
}

// === Utilisateur / Gestionnaire ===

export interface User {
  id: string;
  email: string;
  name: string;
  role: 'portfolio_manager' | 'analyst' | 'admin';
  preferences: UserPreferences;
}

export interface UserPreferences {
  defaultRiskFreeRate: number;
  defaultCurrency: string;
  theme: 'light' | 'dark' | 'system';
}

// === Authentification ===

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface AuthResponse {
  user: User;
  token: string;
  expiresAt: string;
}

// === Analyse de Risque ===

export interface RiskMetrics {
  valueAtRisk: number;      // VaR à 95%
  conditionalVaR: number;   // CVaR / Expected Shortfall
  maxDrawdown: number;      // Perte maximale historique
  beta: number;             // β par rapport au marché
  trackingError: number;    // Écart de suivi
}

// === Moments Statistiques (Point 6 du document) ===

export interface StatisticalMoments {
  mean: number;             // Premier moment
  variance: number;         // Deuxième moment central
  skewness: number;         // Troisième moment normalisé
  kurtosis: number;         // Quatrième moment normalisé (excès)
}

// === API Responses ===

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  hasMore: boolean;
}
