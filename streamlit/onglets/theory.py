from __future__ import annotations

import streamlit as st

from onglets.base import Page
from state import AppState, OptimizationConfig


class TheoryPage(Page):
    name = "📚 Théorie"

    def render(self, state: AppState, config: OptimizationConfig) -> None:
        st.subheader("📚 Théorie Moderne du Portefeuille - Markowitz")
        st.markdown("""
        Cette page présente les concepts clés (μ, σ, Σ, Markowitz, Sharpe, CML, VaR, CVaR).
        """)
        with st.expander("1-2. Rendement et Risque"):
            st.latex(r"\mu_i = E[R_i] = \frac{1}{T}\sum_{t=1}^{T} R_{i,t}")
            st.latex(r"\sigma_i^2 = Var(R_i) = E[(R_i - \mu_i)^2]")
        with st.expander("3-4. Portefeuille et Matrice de Covariance"):
            st.latex(r"\mu_p = \sum_{i=1}^{n} w_i \mu_i = \mathbf{w}'\boldsymbol{\mu}")
            st.latex(r"\sigma_p^2 = \sum_{i=1}^{n}\sum_{j=1}^{n} w_i w_j \sigma_{ij} = \mathbf{w}'\boldsymbol{\Sigma}\mathbf{w}")
        with st.expander("7-8. Problème d'Optimisation"):
            st.latex(r"\min_{\mathbf{w}} \mathbf{w}'\boldsymbol{\Sigma}\mathbf{w}")
            st.latex(r"\text{s.t.} \quad \mathbf{w}'\boldsymbol{\mu} = r^*, \quad \sum i w_i = 1")
