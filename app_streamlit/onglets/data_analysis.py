from __future__ import annotations

import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import pandas as pd

from app_streamlit.onglets.base import Page
from app_streamlit.state import AppState, OptimizationConfig


class DataAnalysisPage(Page):
    name = "📊 Analyse des Données"

    def render(self, state: AppState, config: OptimizationConfig) -> None:
        if state.returns_df is None:
            st.info("👆 Veuillez charger des données dans la barre latérale pour commencer.")
            return

        returns_df = state.returns_df

        # Statistiques descriptives
        st.subheader("📈 Statistiques Descriptives")
        stats_df = pd.DataFrame({
            'Rendement annualisé (%)': returns_df.mean() * 252 * 100,
            'Volatilité annualisée (%)': returns_df.std() * np.sqrt(252) * 100,
            'Sharpe (r_f=2%)': (returns_df.mean() * 252 - 0.02) / (returns_df.std() * np.sqrt(252)),
            'Skewness': returns_df.skew(),
            'Kurtosis': returns_df.kurtosis()
        }).round(3)
        st.dataframe(stats_df, width="stretch")

        # Matrice de corrélation juste en dessous
        st.subheader("🔗 Matrice de Corrélation")
        corr_matrix = returns_df.corr()
        fig_corr = px.imshow(
            corr_matrix,
            labels=dict(color="Corrélation"),
            color_continuous_scale='RdBu_r',
            zmin=-1, zmax=1
        )
        if config.theme == "dark":
            fig_corr.update_layout(template='plotly_dark', paper_bgcolor='#16213e')
        else:
            fig_corr.update_layout(template='plotly', paper_bgcolor='#ffffff')
        st.plotly_chart(fig_corr, config={"responsive": True})

        # Matrice diagonalisee (valeurs propres/vecteurs propres)
        st.subheader("Matrice Diagonalisée (Poids des actifs propres)")
        # Diagonalisation de la matrice de corrélation
        eigvals, eigvecs = np.linalg.eigh(corr_matrix.values)
        # On affiche les valeurs propres (poids des axes principaux)
        eigvals_sorted = np.flip(np.sort(eigvals))
        eigvecs_sorted = eigvecs[:, np.flip(np.argsort(eigvals))]
        poids_df = pd.DataFrame(eigvecs_sorted, columns=[f"Axe {i+1} (λ={eigvals_sorted[i]:.2f})" for i in range(len(eigvals_sorted))], index=corr_matrix.index)
        st.dataframe(poids_df.round(3), width="stretch")
        st.info("La frontière efficiente sera construite sur la base des actifs propres (axes principaux) issus de la diagonalisation de la matrice de corrélation.")

        st.subheader("📊 Distribution des Rendements")
        selected_asset = st.selectbox("Sélectionner un actif", state.selected_assets)
        fig = make_subplots(rows=1, cols=2, subplot_titles=['Histogramme', 'Série temporelle'])
        fig.add_trace(go.Histogram(x=returns_df[selected_asset] * 100, nbinsx=50, marker_color='#e94560'), row=1, col=1)
        fig.add_trace(go.Scatter(y=returns_df[selected_asset].cumsum() * 100, mode='lines',
                                 line=dict(color='#64ffda')), row=1, col=2)
        if config.theme == "dark":
            fig.update_layout(template='plotly_dark', paper_bgcolor='#16213e', plot_bgcolor='#1a1a2e', showlegend=False)
        else:
            fig.update_layout(template='plotly', paper_bgcolor='#ffffff', plot_bgcolor='#ffffff', showlegend=False)
        st.plotly_chart(fig, config={"responsive": True})
