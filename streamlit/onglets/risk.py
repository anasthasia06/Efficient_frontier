from __future__ import annotations

import streamlit as st

from streamlit.onglets.base import Page
from streamlit.state import AppState, OptimizationConfig
from streamlit.services import OptimizationService


class RiskAnalysisPage(Page):
    name = "⚠️ Analyse des Risques"

    def __init__(self):
        self.opt_service = OptimizationService()

    def render(self, state: AppState, config: OptimizationConfig) -> None:
        if state.frontier is None:
            st.info("👆 Calculez d'abord la frontière efficiente.")
            return

        st.subheader("⚠️ Mesures de Risque")
        portfolio_choice = st.radio("Portefeuille à analyser", ["Variance Minimale", "Max Sharpe"], horizontal=True)
        portfolio = state.frontier.min_variance_portfolio if portfolio_choice == "Variance Minimale" else state.frontier.max_sharpe_portfolio

        col1, col2, col3 = st.columns(3)
        with col1:
            var_95 = self.opt_service.var(portfolio.expected_return, portfolio.volatility, 0.95)
            st.metric("VaR 95% (1 jour)", f"{var_95 * 100:.2f}%")
        with col2:
            var_99 = self.opt_service.var(portfolio.expected_return, portfolio.volatility, 0.99)
            st.metric("VaR 99% (1 jour)", f"{var_99 * 100:.2f}%")
        with col3:
            cvar = self.opt_service.cvar(portfolio.expected_return, portfolio.volatility, 0.95)
            st.metric("CVaR 95%", f"{cvar * 100:.2f}%")

        st.markdown("""
        ---
        **Interprétation:**
        - **VaR 95%**: Avec 95% de confiance, la perte journalière ne dépassera pas cette valeur.
        - **VaR 99%**: Niveau de confiance plus élevé, donc perte potentielle plus importante.
        - **CVaR (Expected Shortfall)**: Perte moyenne attendue au-delà de la VaR.
        """)
        st.latex(r"VaR_\alpha = -(\mu_p - z_\alpha \cdot \sigma_p)")
