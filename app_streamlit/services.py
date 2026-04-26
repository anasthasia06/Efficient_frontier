from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf

from app_streamlit.core.optimization import (
    calculate_expected_returns,
    calculate_covariance_matrix,
    compute_efficient_frontier,
    optimize_min_variance,
    optimize_max_sharpe,
    calculate_var,
    calculate_cvar,
)


@dataclass
class MarketDataService:
    """Charge les données de marché (Yahoo Finance)."""

    @st.cache_data(show_spinner=False)
    def load_market_data(self, tickers: List[str], start_date: datetime, end_date: datetime) -> Optional[pd.DataFrame]:
        try:
            with st.spinner("Chargement des données de marché..."):
                data = pd.DataFrame(
                    yf.download(
                        tickers,
                        start=start_date,
                        end=end_date,
                        auto_adjust=False,
                        progress=False,
                        group_by="column",
                    )
                )

                if data.empty:
                    st.error("Aucune donnée récupérée depuis Yahoo Finance.")
                    return None

                # MultiIndex columns (plusieurs tickers)
                if isinstance(data.columns, pd.MultiIndex):
                    level0 = data.columns.get_level_values(0)
                    if "Adj Close" in level0:
                        prices = data["Adj Close"].copy()
                    elif "Close" in level0:
                        st.warning("Adj Close indisponible → utilisation de Close.")
                        prices = data["Close"].copy()
                    else:
                        st.error("Ni 'Adj Close' ni 'Close' disponibles.")
                        return None
                else:
                    # Single ticker
                    if "Adj Close" in data.columns:
                        prices = data[["Adj Close"]].copy()
                    elif "Close" in data.columns:
                        st.warning("Adj Close indisponible → utilisation de Close.")
                        prices = data[["Close"]].copy()
                    else:
                        st.error("Colonnes de prix introuvables.")
                        return None

                prices = prices.dropna()
                if prices.empty:
                    st.error("Les données sont vides après nettoyage.")
                    return None

                return pd.DataFrame(prices)
        except Exception as e:
            st.error(f"Erreur Yahoo Finance : {str(e)}")
            return None


@dataclass
class SyntheticDataService:
    """Génère des données synthétiques de rendements."""

    def generate(self, n_assets: int, n_periods: int, seed: int = 42) -> pd.DataFrame:
        np.random.seed(seed)
        expected_rets = np.random.uniform(0.05, 0.15, n_assets)
        volatilities = np.random.uniform(0.10, 0.35, n_assets)

        returns = np.zeros((n_periods, n_assets))
        for i in range(n_assets):
            returns[:, i] = np.random.normal(
                expected_rets[i] / 252,
                volatilities[i] / np.sqrt(252),
                n_periods,
            )

        asset_names = [f"Actif_{i+1}" for i in range(n_assets)]
        return pd.DataFrame(returns, columns=asset_names)


@dataclass
class OptimizationService:
    """Wrap des fonctions d'optimisation et centralise les annualisations."""

    def expected_returns_annualized(self, returns_array: np.ndarray) -> np.ndarray:
        return calculate_expected_returns(returns_array) * 252

    def covariance_matrix_annualized(self, returns_array: np.ndarray) -> np.ndarray:
        return calculate_covariance_matrix(returns_array) * 252

    def efficient_frontier(self,
                           expected_returns: np.ndarray,
                           cov_matrix: np.ndarray,
                           risk_free_rate: float,
                           num_points: int,
                           allow_short_selling: bool,
                           min_weight: float,
                           max_weight: float):
        return compute_efficient_frontier(
            expected_returns,
            cov_matrix,
            risk_free_rate=risk_free_rate,
            num_points=num_points,
            allow_short_selling=allow_short_selling,
            min_weight=min_weight,
            max_weight=max_weight,
        )

    def min_variance(self, expected_returns: np.ndarray, cov_matrix: np.ndarray,
                     allow_short_selling: bool, min_weight: float, max_weight: float):
        return optimize_min_variance(
            expected_returns,
            cov_matrix,
            target_return=None,
            allow_short_selling=allow_short_selling,
            min_weight=min_weight,
            max_weight=max_weight,
        )

    def max_sharpe(self, expected_returns: np.ndarray, cov_matrix: np.ndarray,
                   risk_free_rate: float, allow_short_selling: bool, min_weight: float, max_weight: float):
        return optimize_max_sharpe(expected_returns, cov_matrix, risk_free_rate, allow_short_selling, min_weight, max_weight)

    def var(self, mu: float, sigma: float, alpha: float = 0.95) -> float:
        return calculate_var(mu, sigma, alpha)

    def cvar(self, mu: float, sigma: float, alpha: float = 0.95) -> float:
        return calculate_cvar(mu, sigma, alpha)
