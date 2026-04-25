from __future__ import annotations

from typing import List

import numpy as np
import plotly.graph_objects as go


class PlotService:
    """Centralise la génération des graphiques Plotly."""

    def efficient_frontier(self, frontier, risk_free_rate: float, theme: str = "dark") -> go.Figure:
        fig = go.Figure()
        risks = [p.portfolio_risk * 100 for p in frontier.points]
        returns = [p.portfolio_return * 100 for p in frontier.points]
        sharpes = [p.sharpe_ratio for p in frontier.points]

        fig.add_trace(go.Scatter(
            x=risks,
            y=returns,
            mode='lines+markers',
            name='Frontière Efficiente',
            line=dict(color='#e94560', width=3),
            marker=dict(size=8, color=sharpes, colorscale='Viridis', showscale=True,
                        colorbar=dict(title='Sharpe')),
            hovertemplate='Risque: %{x:.2f}%<br>Rendement: %{y:.2f}%<extra></extra>'
        ))

        min_var = frontier.min_variance_portfolio
        fig.add_trace(go.Scatter(
            x=[min_var.volatility * 100],
            y=[min_var.expected_return * 100],
            mode='markers',
            name='Variance Minimale',
            marker=dict(size=15, color='#64ffda', symbol='diamond'),
            hovertemplate='Min Variance<br>σ: %{x:.2f}%<br>μ: %{y:.2f}%<extra></extra>'
        ))

        max_sharpe = frontier.max_sharpe_portfolio
        fig.add_trace(go.Scatter(
            x=[max_sharpe.volatility * 100],
            y=[max_sharpe.expected_return * 100],
            mode='markers',
            name='Max Sharpe (Tangent)',
            marker=dict(size=15, color='#ffd93d', symbol='star'),
            hovertemplate='Max Sharpe<br>σ: %{x:.2f}%<br>μ: %{y:.2f}%<br>Sharpe: ' + f'{max_sharpe.sharpe_ratio:.3f}<extra></extra>'
        ))

        max_risk = max(risks) * 1.2
        cml_returns = [risk_free_rate * 100 + max_sharpe.sharpe_ratio * r for r in np.linspace(0, max_risk, 50)]

        fig.add_trace(go.Scatter(
            x=list(np.linspace(0, max_risk, 50)),
            y=cml_returns,
            mode='lines',
            name='Capital Market Line',
            line=dict(color='#ffd93d', width=2, dash='dash'),
        ))

        if theme == "dark":
            fig.update_layout(
                title=dict(text='Frontière Efficiente - Modèle de Markowitz', font=dict(size=20)),
                xaxis_title='Risque (σ) %',
                yaxis_title='Rendement Espéré (μ) %',
                template='plotly_dark',
                paper_bgcolor='#16213e',
                plot_bgcolor='#1a1a2e',
                legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                hovermode='closest'
            )
        else:
            fig.update_layout(
                title=dict(text='Frontière Efficiente - Modèle de Markowitz', font=dict(size=20)),
                xaxis_title='Risque (σ) %',
                yaxis_title='Rendement Espéré (μ) %',
                template='plotly',
                paper_bgcolor='#ffffff',
                plot_bgcolor='#ffffff',
                legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                hovermode='closest'
            )
        return fig

    def weights(self, weights: np.ndarray, asset_names: List[str], title: str, theme: str = "dark") -> go.Figure:
        colors = ['#e94560' if w >= 0 else '#64ffda' for w in weights]
        fig = go.Figure(go.Bar(
            x=asset_names,
            y=weights * 100,
            marker_color=colors,
            text=[f'{w*100:.1f}%' for w in weights],
            textposition='outside'
        ))
        if theme == "dark":
            fig.update_layout(
                title=title,
                xaxis_title='Actifs',
                yaxis_title='Allocation (%)',
                template='plotly_dark',
                paper_bgcolor='#16213e',
                plot_bgcolor='#1a1a2e',
            )
        else:
            fig.update_layout(
                title=title,
                xaxis_title='Actifs',
                yaxis_title='Allocation (%)',
                template='plotly',
                paper_bgcolor='#ffffff',
                plot_bgcolor='#ffffff',
            )
        return fig
