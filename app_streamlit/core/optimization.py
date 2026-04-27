"""
Module d'optimisation de portefeuille - Modèle de Markowitz
Implémentation avancée des 14 points du document prog_finance_fr_v2

Ce module fournit les fonctions mathématiques pour:
- Calcul des rendements espérés et de la volatilité
- Construction de la matrice de covariance
- Optimisation quadratique sous contraintes
- Calcul de la frontière efficiente
- Mesures de risque (VaR, CVaR, Sharpe)
"""

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import minimize
from typing import Optional, Dict, List
from dataclasses import dataclass


@dataclass
class PortfolioMetrics:
    """Métriques d'un portefeuille optimisé."""
    expected_return: float      # μ_p = w'μ
    volatility: float           # σ_p = √(w'Σw)
    variance: float             # σ²_p = w'Σw
    sharpe_ratio: float         # (μ_p - r_f) / σ_p
    weights: NDArray[np.float64]  # Vecteur des allocations


@dataclass
class EfficientFrontierPoint:
    """Point sur la frontière efficiente."""
    target_return: float
    portfolio_return: float
    portfolio_risk: float
    weights: NDArray[np.float64]
    sharpe_ratio: float


@dataclass
class EfficientFrontier:
    """Frontière efficiente complète."""
    points: List[EfficientFrontierPoint]
    min_variance_portfolio: PortfolioMetrics
    max_sharpe_portfolio: PortfolioMetrics
    
    
def calculate_returns(prices: NDArray[np.float64]) -> NDArray[np.float64]:
    """
    Calcule les rendements logarithmiques à partir des prix.
    
    R_t = ln(P_t / P_{t-1})
    
    Args:
        prices: Matrice des prix (T x N) - T périodes, N actifs
        
    Returns:
        Matrice des rendements (T-1 x N)
    """
    return np.log(prices[1:] / prices[:-1])


def calculate_expected_returns(returns: NDArray[np.float64]) -> NDArray[np.float64]:
    """
    Calcule le vecteur des rendements espérés (moyenne).
    
    μ_i = E[R_i] = (1/T) Σ R_{i,t}
    
    Point 1 du document: Espérance des rendements
    
    Args:
        returns: Matrice des rendements (T x N)
        
    Returns:
        Vecteur des rendements espérés (N,)
    """
    return np.mean(returns, axis=0)


def calculate_covariance_matrix(returns: NDArray[np.float64]) -> NDArray[np.float64]:
    """
    Calcule la matrice de covariance Σ.
    
    Σ_{i,j} = Cov(R_i, R_j) = E[(R_i - μ_i)(R_j - μ_j)]
    
    Point 3 du document: Matrice de covariance
    
    Args:
        returns: Matrice des rendements (T x N)
        
    Returns:
        Matrice de covariance (N x N)
    """
    return np.cov(returns, rowvar=False)


def calculate_correlation_matrix(cov_matrix: NDArray[np.float64]) -> NDArray[np.float64]:
    """
        Calcule la matrice de corrélation à partir de la matrice de covariance.
        
        ρ_{i,j} = Σ_{i,j} / (σ_i × σ_j)
        
        Args:
            cov_matrix: Matrice de covariance (N x N)
            
        Returns:
            Matrice de corrélation (N x N)

    """
    std_devs = np.sqrt(np.diag(cov_matrix))
    outer_std = np.outer(std_devs, std_devs)
    return cov_matrix / outer_std


def calculate_portfolio_metrics(
    weights: NDArray[np.float64],
    expected_returns: NDArray[np.float64],
    cov_matrix: NDArray[np.float64],
    risk_free_rate: float = 0.0
) -> PortfolioMetrics:
    """ 
        Calcule les métriques d'un portefeuille.
        
        Point 4 du document:
        - Rendement espéré: μ_p = w'μ = Σ w_i × μ_i
        - Variance: σ²_p = w'Σw
        - Volatilité: σ_p = √(w'Σw)
        
        Point 9: Ratio de Sharpe
        - S = (μ_p - r_f) / σ_p
        
        Args:
            weights: Vecteur des poids (N,)
            expected_returns: Vecteur des rendements espérés (N,)
            cov_matrix: Matrice de covariance (N x N)
            risk_free_rate: Taux sans risque r_f
            
        Returns:
            PortfolioMetrics avec toutes les métriques calculées
    """
    # Rendement espéré du portefeuille
    port_return = np.dot(weights, expected_returns)
    
    # Variance du portefeuille
    port_variance = np.dot(weights, np.dot(cov_matrix, weights))
    
    # Volatilité (écart-type)
    port_volatility = np.sqrt(port_variance)
    
    # Ratio de Sharpe
    sharpe = (port_return - risk_free_rate) / port_volatility if port_volatility > 0 else 0.0
    
    return PortfolioMetrics(
        expected_return=port_return,
        volatility=port_volatility,
        variance=port_variance,
        sharpe_ratio=sharpe,
        weights=weights.copy()
    )


def optimize_min_variance(
    expected_returns: NDArray[np.float64],
    cov_matrix: NDArray[np.float64],
    target_return: Optional[float] = None,
    allow_short_selling: bool = False,
    min_weight: float = 0.0,
    max_weight: float = 1.0,
    risk_free_rate: float = 0.0
) -> PortfolioMetrics:
    """
    Optimisation de Markowitz: minimiser la variance pour un rendement cible.
    
    Points 7-8 du document:
    
    min  w'Σw
    s.t. w'μ = r*        (contrainte de rendement)
         Σw_i = 1        (contrainte de budget)
         w_min ≤ w_i ≤ w_max  (contraintes de bornes)
    
    Args:
        expected_returns: Vecteur des rendements espérés (N,)
        cov_matrix: Matrice de covariance (N x N)
        target_return: Rendement cible r* (optionnel)
        allow_short_selling: Autoriser les poids négatifs
        min_weight: Poids minimum par actif
        max_weight: Poids maximum par actif
        risk_free_rate: Taux sans risque
        
    Returns:
        PortfolioMetrics du portefeuille optimal
    """
    n_assets = len(expected_returns)

    # Fonction objectif: variance du portefeuille
    def portfolio_variance(weights: NDArray) -> float:
        return np.dot(weights, np.dot(cov_matrix, weights))

    # Contrainte: somme des poids = 1
    constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]

    # Contrainte de rendement cible si spécifiée
    if target_return is not None:
        constraints.append({
            'type': 'eq',
            'fun': lambda w: np.dot(w, expected_returns) - target_return
        })

    # Bornes des poids
    if allow_short_selling:
        bounds = tuple((min_weight, max_weight) for _ in range(n_assets))
    else:
        bounds = tuple((max(0, min_weight), max_weight) for _ in range(n_assets))
 
    # Point de départ: répartition équipondérée
    initial_weights = np.ones(n_assets) / n_assets
 
    # Optimisation
    result = minimize(
        portfolio_variance,
        initial_weights,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints
    )
 
    if not result.success:
        # Fallback: retourner le portefeuille équipondéré
        return calculate_portfolio_metrics(
            initial_weights, expected_returns, cov_matrix, risk_free_rate
        )
 
    return calculate_portfolio_metrics(
        result.x, expected_returns, cov_matrix, risk_free_rate
    )


def optimize_max_sharpe(
    expected_returns: NDArray[np.float64],
    cov_matrix: NDArray[np.float64],
    risk_free_rate: float = 0.0,
    allow_short_selling: bool = False,
    min_weight: float = 0.0,
    max_weight: float = 1.0
) -> PortfolioMetrics:
    """
    Trouve le portefeuille tangent (maximum ratio de Sharpe).
 
    Point 9-10 du document:
 
    max  (w'μ - r_f) / √(w'Σw)
    s.t. Σw_i = 1
         w_min ≤ w_i ≤ w_max
 
    Args:
        expected_returns: Vecteur des rendements espérés
        cov_matrix: Matrice de covariance
        risk_free_rate: Taux sans risque
        allow_short_selling: Autoriser les ventes à découvert
        min_weight: Poids minimum
        max_weight: Poids maximum
 
    Returns:
        PortfolioMetrics du portefeuille tangent
    """
    n_assets = len(expected_returns)
 
    # Fonction objectif: négatif du Sharpe (on minimise)
    def neg_sharpe(weights: NDArray) -> float:
        port_return = np.dot(weights, expected_returns)
        port_vol = np.sqrt(np.dot(weights, np.dot(cov_matrix, weights)))
        if port_vol == 0:
            return 0
        return -(port_return - risk_free_rate) / port_vol
 
    # Contraintes
    constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]
 
    # Bornes
    if allow_short_selling:
        bounds = tuple((min_weight, max_weight) for _ in range(n_assets))
    else:
        bounds = tuple((max(0, min_weight), max_weight) for _ in range(n_assets))
 
    # Optimisation
    initial_weights = np.ones(n_assets) / n_assets
 
    result = minimize(
        neg_sharpe,
        initial_weights,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints
    )
 
    return calculate_portfolio_metrics(
        result.x if result.success else initial_weights,
        expected_returns,
        cov_matrix,
        risk_free_rate
    )


def compute_efficient_frontier(
    expected_returns: NDArray[np.float64],
    cov_matrix: NDArray[np.float64],
    risk_free_rate: float = 0.0,
    num_points: int = 50,
    allow_short_selling: bool = False,
    min_weight: float = 0.0,
    max_weight: float = 1.0
) -> EfficientFrontier:
    """
    Calcule la frontière efficiente complète.
 
    Point 11 du document: Frontière efficiente
 
    Pour chaque rendement cible entre min et max, trouve le portefeuille
    de variance minimale.
 
    Args:
        expected_returns: Vecteur des rendements espérés
        cov_matrix: Matrice de covariance
        risk_free_rate: Taux sans risque
        num_points: Nombre de points sur la frontière
        allow_short_selling: Autoriser les ventes à découvert
        min_weight: Poids minimum
        max_weight: Poids maximum
 
    Returns:
        EfficientFrontier avec tous les points et portefeuilles clés
    """
    # Bornes des rendements
    if allow_short_selling:
        min_return = np.min(expected_returns) * 0.5
        max_return = np.max(expected_returns) * 1.5
    else:
        min_return = np.min(expected_returns)
        max_return = np.max(expected_returns)
 
    target_returns = np.linspace(min_return, max_return, num_points)
 
    points: List[EfficientFrontierPoint] = []
 
    for target in target_returns:
        try:
            portfolio = optimize_min_variance(
                expected_returns,
                cov_matrix,
                target_return=target,
                allow_short_selling=allow_short_selling,
                min_weight=min_weight,
                max_weight=max_weight,
                risk_free_rate=risk_free_rate
            )
            
            points.append(EfficientFrontierPoint(
                target_return=target,
                portfolio_return=portfolio.expected_return,
                portfolio_risk=portfolio.volatility,
                weights=portfolio.weights,
                sharpe_ratio=portfolio.sharpe_ratio
            ))
        except Exception:
            continue
    
    # Filtrer la partie efficiente (rendement croissant avec risque)
    efficient_points = filter_efficient_points(points)
    
    # Portefeuille de variance minimale globale
    min_var_portfolio = optimize_min_variance(
        expected_returns,
        cov_matrix,
        target_return=None,
        allow_short_selling=allow_short_selling,
        min_weight=min_weight,
        max_weight=max_weight,
        risk_free_rate=risk_free_rate
    )
    
    # Portefeuille tangent (max Sharpe)
    max_sharpe_portfolio = optimize_max_sharpe(
        expected_returns,
        cov_matrix,
        risk_free_rate=risk_free_rate,
        allow_short_selling=allow_short_selling,
        min_weight=min_weight,
        max_weight=max_weight
    )
    
    return EfficientFrontier(
        points=efficient_points,
        min_variance_portfolio=min_var_portfolio,
        max_sharpe_portfolio=max_sharpe_portfolio
    )


def filter_efficient_points(points: List[EfficientFrontierPoint]) -> List[EfficientFrontierPoint]:
    """
    Filtre les points pour ne garder que la frontière efficiente.
    
    Un point est efficient si aucun autre point n'a un rendement supérieur
    pour le même niveau de risque.
    """
    if not points:
        return []
    
    # Trier par risque croissant
    sorted_points = sorted(points, key=lambda p: p.portfolio_risk)
    
    efficient = []
    max_return = float('-inf')
    
    for point in sorted_points:
        if point.portfolio_return > max_return:
            efficient.append(point)
            max_return = point.portfolio_return
    
    return efficient


def calculate_var(
    portfolio_return: float,
    portfolio_volatility: float,
    confidence_level: float = 0.95,
    horizon: int = 1
) -> float:
    """
    Calcule la Value at Risk (VaR) paramétrique.
    
    Point 12 du document: Mesures de risque
    
    VaR_α = -(μ_p - z_α × σ_p) × √T
    
    où z_α est le quantile de la loi normale standard.
    
    Args:
        portfolio_return: Rendement espéré
        portfolio_volatility: Volatilité
        confidence_level: Niveau de confiance (0.95 = 95%)
        horizon: Horizon en jours
        
    Returns:
        VaR (perte maximale attendue)
    """
    from scipy.stats import norm
    z_alpha = norm.ppf(confidence_level)
    return -(portfolio_return - z_alpha * portfolio_volatility) * np.sqrt(horizon)

def calculate_cvar(
    portfolio_return: float,
    portfolio_volatility: float,
    confidence_level: float = 0.95
) -> float:
    """
    Calcule la Conditional Value at Risk (CVaR / Expected Shortfall).
    
    CVaR = μ_p - σ_p × φ(z_α) / (1 - α)
    
    où φ est la densité de la loi normale standard.
    
    Args:
        portfolio_return: Rendement espéré
        portfolio_volatility: Volatilité
        confidence_level: Niveau de confiance
        
    Returns:
        CVaR (perte moyenne au-delà de la VaR)
    """
    from scipy.stats import norm
    z_alpha = norm.ppf(confidence_level)
    phi = norm.pdf(z_alpha)
    cvar = -(portfolio_return - portfolio_volatility * phi / (1 - confidence_level))
    return float(cvar)

def calculate_statistical_moments(returns: NDArray[np.float64]) -> Dict[str, float]:
    """
    Calcule les moments statistiques des rendements.
    
    Point 6 du document: Moments statistiques
    
    - Moyenne (1er moment)
    - Variance (2ème moment central)
    - Skewness (asymétrie, 3ème moment normalisé)
    - Kurtosis (aplatissement, 4ème moment normalisé - 3)
    
    Args:
        returns: Série de rendements
        
    Returns:
        Dictionnaire avec les 4 moments
    """
    from scipy.stats import skew, kurtosis
    
    return {
        'mean': float(np.mean(returns)),
        'variance': float(np.var(returns, ddof=1)),
        'skewness': float(skew(returns)),
        'kurtosis': float(kurtosis(returns, fisher=True))  # Excès de kurtosis
    }
