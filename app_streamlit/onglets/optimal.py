from __future__ import annotations

import streamlit as st
import pandas as pd

from app_streamlit.onglets.base import Page
from app_streamlit.state import AppState, OptimizationConfig
from app_streamlit.services import OptimizationService
from app_streamlit.plots import PlotService


class OptimalPortfoliosPage(Page):
    name = "💼 Portefeuilles Optimaux"

    def __init__(self):
        self.opt_service = OptimizationService()
        self.plot_service = PlotService()

    def render(self, state: AppState, config: OptimizationConfig) -> None:
        if state.frontier is None:
            st.info("👆 Calculez d'abord la frontière efficiente dans l'onglet précédent.")
            return

        frontier = state.frontier
        # Utiliser les actifs mémorisés lors du calcul de la frontière pour garantir la cohérence
        assets = state.frontier_assets if state.frontier_assets else (list(state.returns_df.columns) if state.returns_df is not None else [])
        # Sécurité: aligner la longueur des noms avec les poids
        n_weights = len(frontier.min_variance_portfolio.weights)
        if len(assets) != n_weights:
            assets = [f"Actif {i+1}" for i in range(n_weights)]

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("💎 Portefeuille Variance Minimale")
            min_var = frontier.min_variance_portfolio
            st.markdown(f"""
            | Métrique | Valeur |
            |----------|--------|
            | Rendement espéré (μ) | **{min_var.expected_return * 100:.2f}%** |
            | Volatilité (σ) | **{min_var.volatility * 100:.2f}%** |
            | Ratio de Sharpe | **{min_var.sharpe_ratio:.3f}** |
            | VaR 95% | **{self.opt_service.var(min_var.expected_return, min_var.volatility) * 100:.2f}%** |
            """)
            st.plotly_chart(
                self.plot_service.weights(min_var.weights, assets, "Allocations - Min Variance", theme=config.theme),
                config={"responsive": True}
            )

        with col2:
            st.subheader("⭐ Portefeuille Tangent (Max Sharpe)")
            max_sharpe = frontier.max_sharpe_portfolio
            st.markdown(f"""
            | Métrique | Valeur |
            |----------|--------|
            | Rendement espéré (μ) | **{max_sharpe.expected_return * 100:.2f}%** |
            | Volatilité (σ) | **{max_sharpe.volatility * 100:.2f}%** |
            | Ratio de Sharpe | **{max_sharpe.sharpe_ratio:.3f}** |
            | VaR 95% | **{self.opt_service.var(max_sharpe.expected_return, max_sharpe.volatility) * 100:.2f}%** |
            """)
            st.plotly_chart(
                self.plot_service.weights(max_sharpe.weights, assets, "Allocations - Max Sharpe", theme=config.theme),
                config={"responsive": True}
            )

        st.subheader("📊 Comparaison des Portefeuilles")
        comparison_df = pd.DataFrame({
            'Min Variance': frontier.min_variance_portfolio.weights * 100,
            'Max Sharpe': frontier.max_sharpe_portfolio.weights * 100
        }, index=assets)
        st.dataframe(comparison_df.style.format("{:.1f}%"), width="stretch")
