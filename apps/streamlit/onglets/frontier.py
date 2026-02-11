from __future__ import annotations

import streamlit as st

from onglets.base import Page
from state import AppState, OptimizationConfig
from services import OptimizationService
from plots import PlotService


class FrontierPage(Page):
    name = "🎯 Frontière Efficiente"

    def __init__(self):
        self.opt_service = OptimizationService()
        self.plot_service = PlotService()

    def render(self, state: AppState, config: OptimizationConfig) -> None:
        if state.returns_df is None:
            st.info("👆 Veuillez charger des données pour calculer la frontière efficiente.")
            return

        if st.button("🚀 Calculer la Frontière Efficiente", type="primary"):
            with st.spinner("Optimisation en cours..."):
                returns_array = state.returns_df.values
                expected_returns = self.opt_service.expected_returns_annualized(returns_array)
                cov_matrix = self.opt_service.covariance_matrix_annualized(returns_array)
                frontier = self.opt_service.efficient_frontier(
                    expected_returns,
                    cov_matrix,
                    risk_free_rate=config.risk_free_rate,
                    num_points=config.num_frontier_points,
                    allow_short_selling=config.allow_short,
                    min_weight=config.min_weight,
                    max_weight=config.max_weight,
                )
                state.frontier = frontier
                st.success("✅ Frontière efficiente calculée!")

        if state.frontier is not None:
            fig = self.plot_service.efficient_frontier(state.frontier, config.risk_free_rate, theme=config.theme)
            st.plotly_chart(fig, config={"responsive": True})
