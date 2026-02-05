/**
 * Service d'optimisation de portefeuille - Algorithme de Markowitz
 * Implémentation des calculs basés sur les 14 points du document
 */

import type {
  Asset,
  AssetReturns,
  CovarianceMatrix,
  PortfolioWeights,
  PortfolioMetrics,
  OptimizationConstraints,
  EfficientFrontier,
  EfficientFrontierPoint,
  StatisticalMoments,
} from '@/types/portfolio';

/**
 * Calcule l'espérance (moyenne) des rendements
 * Point 1: E[R] = μ
 */
export function calculateExpectedReturn(returns: number[]): number {
  if (returns.length === 0) return 0;
  return returns.reduce((sum, r) => sum + r, 0) / returns.length;
}

/**
 * Calcule la variance des rendements
 * Point 2: Var(R) = E[(R - μ)²]
 */
export function calculateVariance(returns: number[], mean?: number): number {
  if (returns.length < 2) return 0;
  const mu = mean ?? calculateExpectedReturn(returns);
  const squaredDiffs = returns.map((r) => Math.pow(r - mu, 2));
  return squaredDiffs.reduce((sum, d) => sum + d, 0) / (returns.length - 1);
}

/**
 * Calcule l'écart-type (volatilité)
 * σ = √Var(R)
 */
export function calculateVolatility(returns: number[]): number {
  return Math.sqrt(calculateVariance(returns));
}

/**
 * Calcule les moments statistiques
 * Point 6: Moments d'ordre supérieur
 */
export function calculateMoments(returns: number[]): StatisticalMoments {
  const n = returns.length;
  if (n < 4) {
    return { mean: 0, variance: 0, skewness: 0, kurtosis: 0 };
  }

  const mean = calculateExpectedReturn(returns);
  const variance = calculateVariance(returns, mean);
  const std = Math.sqrt(variance);

  // Skewness (asymétrie)
  const skewness =
    returns.reduce((sum, r) => sum + Math.pow((r - mean) / std, 3), 0) / n;

  // Kurtosis (excès de kurtosis)
  const kurtosis =
    returns.reduce((sum, r) => sum + Math.pow((r - mean) / std, 4), 0) / n - 3;

  return { mean, variance, skewness, kurtosis };
}

/**
 * Calcule la covariance entre deux séries de rendements
 * Cov(R_i, R_j) = E[(R_i - μ_i)(R_j - μ_j)]
 */
export function calculateCovariance(
  returns1: number[],
  returns2: number[]
): number {
  const n = Math.min(returns1.length, returns2.length);
  if (n < 2) return 0;

  const mean1 = calculateExpectedReturn(returns1.slice(0, n));
  const mean2 = calculateExpectedReturn(returns2.slice(0, n));

  let cov = 0;
  for (let i = 0; i < n; i++) {
    cov += (returns1[i] - mean1) * (returns2[i] - mean2);
  }

  return cov / (n - 1);
}

/**
 * Construit la matrice de covariance Σ
 * Point 3: Σ est la matrice de covariance des actifs
 */
export function buildCovarianceMatrix(
  assetsReturns: AssetReturns[]
): CovarianceMatrix {
  const n = assetsReturns.length;
  const matrix: number[][] = [];
  const correlationMatrix: number[][] = [];
  const assetIds = assetsReturns.map((a) => a.assetId);

  // Calculer les volatilités
  const volatilities = assetsReturns.map((a) => a.volatility);

  for (let i = 0; i < n; i++) {
    matrix[i] = [];
    correlationMatrix[i] = [];
    for (let j = 0; j < n; j++) {
      const cov = calculateCovariance(
        assetsReturns[i].returns,
        assetsReturns[j].returns
      );
      matrix[i][j] = cov;

      // Corrélation: ρ_ij = Cov(i,j) / (σ_i × σ_j)
      if (volatilities[i] > 0 && volatilities[j] > 0) {
        correlationMatrix[i][j] = cov / (volatilities[i] * volatilities[j]);
      } else {
        correlationMatrix[i][j] = i === j ? 1 : 0;
      }
    }
  }

  return { assetIds, matrix, correlationMatrix };
}

/**
 * Calcule les métriques du portefeuille
 * Point 4: μ_p = w'μ et σ²_p = w'Σw
 */
export function calculatePortfolioMetrics(
  weights: number[],
  expectedReturns: number[],
  covMatrix: number[][],
  riskFreeRate: number = 0
): PortfolioMetrics {
  const n = weights.length;

  // Rendement espéré: μ_p = Σ w_i × μ_i
  let expectedReturn = 0;
  for (let i = 0; i < n; i++) {
    expectedReturn += weights[i] * expectedReturns[i];
  }

  // Variance: σ²_p = w'Σw
  let variance = 0;
  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
      variance += weights[i] * weights[j] * covMatrix[i][j];
    }
  }

  const volatility = Math.sqrt(variance);

  // Ratio de Sharpe: (μ_p - r_f) / σ_p
  const sharpeRatio = volatility > 0 ? (expectedReturn - riskFreeRate) / volatility : 0;

  return { expectedReturn, variance, volatility, sharpeRatio };
}

/**
 * Optimisation de Markowitz - Trouver les poids optimaux
 * Point 7-8: Minimiser σ²_p sous contrainte de rendement cible
 * 
 * Utilise une approche simplifiée par grille pour l'application mobile.
 * Pour une implémentation complète, utiliser un solver QP.
 */
export function optimizePortfolio(
  expectedReturns: number[],
  covMatrix: number[][],
  constraints: OptimizationConstraints,
  numPoints: number = 50
): EfficientFrontier {
  const n = expectedReturns.length;
  const { minWeight = 0, maxWeight = 1, riskFreeRate = 0 } = constraints;

  // Trouver les bornes de rendement
  const minReturn = Math.min(...expectedReturns);
  const maxReturn = Math.max(...expectedReturns);

  const points: EfficientFrontierPoint[] = [];

  // Pour chaque rendement cible, trouver le portefeuille de variance minimale
  for (let i = 0; i <= numPoints; i++) {
    const targetReturn = minReturn + (i / numPoints) * (maxReturn - minReturn);

    // Optimisation par recherche de grille (simplifié pour mobile)
    const optimalWeights = findMinVarianceWeights(
      expectedReturns,
      covMatrix,
      targetReturn,
      minWeight,
      maxWeight
    );

    if (optimalWeights) {
      const metrics = calculatePortfolioMetrics(
        optimalWeights,
        expectedReturns,
        covMatrix,
        riskFreeRate
      );

      points.push({
        targetReturn,
        portfolioReturn: metrics.expectedReturn,
        portfolioRisk: metrics.volatility,
        weights: optimalWeights,
        sharpeRatio: metrics.sharpeRatio,
      });
    }
  }

  // Filtrer pour garder seulement la frontière efficiente (partie supérieure)
  const efficientPoints = filterEfficientFrontier(points);

  // Trouver le portefeuille de variance minimale
  const minVariancePortfolio = efficientPoints.reduce((min, p) =>
    p.portfolioRisk < min.portfolioRisk ? p : min
  );

  // Trouver le portefeuille tangent (max Sharpe)
  const maxSharpePortfolio = efficientPoints.reduce((max, p) =>
    p.sharpeRatio > max.sharpeRatio ? p : max
  );

  return {
    points: efficientPoints,
    minVariancePortfolio,
    maxSharpePortfolio,
  };
}

/**
 * Recherche des poids de variance minimale pour un rendement cible
 * Approche simplifiée par échantillonnage aléatoire
 */
function findMinVarianceWeights(
  expectedReturns: number[],
  covMatrix: number[][],
  targetReturn: number,
  minWeight: number,
  maxWeight: number,
  iterations: number = 1000
): number[] | null {
  const n = expectedReturns.length;
  let bestWeights: number[] | null = null;
  let bestVariance = Infinity;

  for (let iter = 0; iter < iterations; iter++) {
    // Générer des poids aléatoires
    const weights = generateRandomWeights(n, minWeight, maxWeight);

    // Calculer le rendement
    let portfolioReturn = 0;
    for (let i = 0; i < n; i++) {
      portfolioReturn += weights[i] * expectedReturns[i];
    }

    // Vérifier la contrainte de rendement (tolérance de 0.5%)
    if (Math.abs(portfolioReturn - targetReturn) > 0.005) continue;

    // Calculer la variance
    let variance = 0;
    for (let i = 0; i < n; i++) {
      for (let j = 0; j < n; j++) {
        variance += weights[i] * weights[j] * covMatrix[i][j];
      }
    }

    if (variance < bestVariance) {
      bestVariance = variance;
      bestWeights = [...weights];
    }
  }

  return bestWeights;
}

/**
 * Génère des poids aléatoires qui somment à 1
 */
function generateRandomWeights(
  n: number,
  minWeight: number,
  maxWeight: number
): number[] {
  const weights: number[] = [];
  let remaining = 1;

  for (let i = 0; i < n - 1; i++) {
    const maxPossible = Math.min(maxWeight, remaining - (n - i - 1) * minWeight);
    const minPossible = Math.max(minWeight, remaining - (n - i - 1) * maxWeight);
    const w = minPossible + Math.random() * (maxPossible - minPossible);
    weights.push(w);
    remaining -= w;
  }
  weights.push(remaining);

  return weights;
}

/**
 * Filtre les points pour ne garder que la frontière efficiente
 */
function filterEfficientFrontier(
  points: EfficientFrontierPoint[]
): EfficientFrontierPoint[] {
  // Trier par risque croissant
  const sorted = [...points].sort((a, b) => a.portfolioRisk - b.portfolioRisk);

  // Garder seulement les points où le rendement augmente
  const efficient: EfficientFrontierPoint[] = [];
  let maxReturn = -Infinity;

  for (const point of sorted) {
    if (point.portfolioReturn > maxReturn) {
      efficient.push(point);
      maxReturn = point.portfolioReturn;
    }
  }

  return efficient;
}

/**
 * Calcule la Value at Risk (VaR) paramétrique
 * Point 12: Mesures de risque
 */
export function calculateVaR(
  portfolioReturn: number,
  portfolioVolatility: number,
  confidenceLevel: number = 0.95,
  horizon: number = 1
): number {
  // Quantile de la loi normale pour le niveau de confiance
  const zScores: Record<number, number> = {
    0.9: 1.282,
    0.95: 1.645,
    0.99: 2.326,
  };
  const z = zScores[confidenceLevel] || 1.645;

  // VaR = -(μ - z × σ) × √T
  return -(portfolioReturn - z * portfolioVolatility) * Math.sqrt(horizon);
}

/**
 * Calcule le ratio de Sharpe
 * Point 9: S = (μ_p - r_f) / σ_p
 */
export function calculateSharpeRatio(
  portfolioReturn: number,
  portfolioVolatility: number,
  riskFreeRate: number
): number {
  if (portfolioVolatility === 0) return 0;
  return (portfolioReturn - riskFreeRate) / portfolioVolatility;
}
