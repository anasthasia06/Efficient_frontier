"""
Application Streamlit - Portfolio Optimizer
Outil avancé d'optimisation de portefeuille basé sur le modèle de Markowitz

Implémente les 14 points du document prog_finance_fr_v2:
1. Espérance des rendements
2. Variance et écart-type
3. Matrice de covariance
4. Rendement et risque du portefeuille
5. Copules (analyse de dépendance)
6. Moments statistiques
7-8. Optimisation de Markowitz
9. Ratio de Sharpe
10. Portefeuille tangent
11. Frontière efficiente
12. Mesures de risque (VaR, CVaR)
13. Algorithmes pratiques
14. Applications
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Optional, List, Dict
import yfinance as yf
from datetime import datetime, timedelta

# Import du module d'optimisation
from core.optimization import (
    calculate_returns,
    calculate_expected_returns,
    calculate_covariance_matrix,
    calculate_correlation_matrix,
    calculate_portfolio_metrics,
    compute_efficient_frontier,
    optimize_min_variance,
    optimize_max_sharpe,
    calculate_var,
    calculate_cvar,
    calculate_statistical_moments
)


# Configuration de la page
st.set_page_config(
    page_title="Portfolio Optimizer - Markowitz",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #e94560;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #8892b0;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #1a1a2e;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #e94560;
    }
    .formula {
        font-family: monospace;
        background-color: #0f0f23;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        color: #64ffda;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1a1a2e;
        border-radius: 4px 4px 0 0;
        color: #ccd6f6;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialise l'état de session."""
    if 'prices_df' not in st.session_state:
        st.session_state.prices_df = None
    if 'returns_df' not in st.session_state:
        st.session_state.returns_df = None
    if 'frontier' not in st.session_state:
        st.session_state.frontier = None
    if 'selected_assets' not in st.session_state:
        st.session_state.selected_assets = []

@st.cache_data(show_spinner=False)
def load_market_data(
    tickers: List[str],
    start_date: datetime,
    end_date: datetime
) -> Optional[pd.DataFrame]:
    """
    Charge les données Yahoo Finance de manière robuste.
    Compatible mono/multi tickers + nouvelles versions yfinance.
    """

    try:
        with st.spinner("Chargement des données de marché..."):
            data = pd.DataFrame()
            data = pd.DataFrame(yf.download(tickers,
                               start=start_date,
                               end=end_date,
                               auto_adjust=False,
                               progress=False,
                               group_by="column"
            ))

            if data.empty:
                st.error("Aucune donnée récupérée depuis Yahoo Finance.")
                return None

            # -----------------------------
            # CAS 1 : plusieurs tickers
            # -----------------------------
            if isinstance(data.columns, pd.MultiIndex):

                # Si Adj Close existe → on le prend
                if "Adj Close" in data.columns.get_level_values(0):
                    prices = data["Adj Close"]

                # Sinon fallback sur Close
                elif "Close" in data.columns.get_level_values(0):
                    st.warning("Adj Close indisponible → utilisation de Close.")
                    prices = data["Close"]

                else:
                    st.error("Ni 'Adj Close' ni 'Close' disponibles.")
                    return None

            # -----------------------------
            # CAS 2 : 1 seul ticker
            # -----------------------------
            else:
                prices = pd.DataFrame()
                if "Adj Close" in data.columns:
                    prices = data[["Adj Close"]]
                elif "Close" in data.columns:
                    st.warning("Adj Close indisponible → utilisation de Close.")
                    prices = data[["Close"]]
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


def create_efficient_frontier_plot(frontier, risk_free_rate: float) -> go.Figure:
    """
    Crée le graphique de la frontière efficiente.

    Args:
        frontier: Objet EfficientFrontier
        risk_free_rate: Taux sans risque

    Returns:
        Figure Plotly
    """
    fig = go.Figure()

    # Frontière efficiente
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

    # Portefeuille de variance minimale
    min_var = frontier.min_variance_portfolio
    fig.add_trace(go.Scatter(
        x=[min_var.volatility * 100],
        y=[min_var.expected_return * 100],
        mode='markers',
        name='Variance Minimale',
        marker=dict(size=15, color='#64ffda', symbol='diamond'),
        hovertemplate='Min Variance<br>σ: %{x:.2f}%<br>μ: %{y:.2f}%<extra></extra>'
    ))

    # Portefeuille tangent (max Sharpe)
    max_sharpe = frontier.max_sharpe_portfolio
    fig.add_trace(go.Scatter(
        x=[max_sharpe.volatility * 100],
        y=[max_sharpe.expected_return * 100],
        mode='markers',
        name='Max Sharpe (Tangent)',
        marker=dict(size=15, color='#ffd93d', symbol='star'),
        hovertemplate='Max Sharpe<br>σ: %{x:.2f}%<br>μ: %{y:.2f}%<br>Sharpe: ' + 
                     f'{max_sharpe.sharpe_ratio:.3f}<extra></extra>'
    ))

    # Capital Market Line
    max_risk = max(risks) * 1.2
    cml_returns = [risk_free_rate * 100 + max_sharpe.sharpe_ratio * r for r in np.linspace(0, max_risk, 50)]

    fig.add_trace(go.Scatter(
        x=list(np.linspace(0, max_risk, 50)),
        y=cml_returns,
        mode='lines',
        name='Capital Market Line',
        line=dict(color='#ffd93d', width=2, dash='dash'),
    ))

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

    return fig


def create_weights_plot(weights: np.ndarray, asset_names: List[str], title: str) -> go.Figure:
    """Crée un graphique en barres des allocations."""
    colors = ['#e94560' if w >= 0 else '#64ffda' for w in weights]

    fig = go.Figure(go.Bar(
        x=asset_names,
        y=weights * 100,
        marker_color=colors,
        text=[f'{w*100:.1f}%' for w in weights],
        textposition='outside'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title='Actifs',
        yaxis_title='Allocation (%)',
        template='plotly_dark',
        paper_bgcolor='#16213e',
        plot_bgcolor='#1a1a2e',
    )

    return fig


def main():
    """Application principale Streamlit."""
    init_session_state()
    
    # En-tête
    st.markdown('<p class="main-header">📈 Portfolio Optimizer</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Optimisation de Portefeuille - Théorie Moderne de Markowitz</p>', 
                unsafe_allow_html=True)

    # Mode OOP désactivé pour le test: utilisez app_oop.py pour lancer l'OOP
    
    # Sidebar - Configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Mode de données
        data_mode = st.radio(
            "Source des données",
            ["Données de marché (Yahoo Finance)", "Données synthétiques (démo)"]
        )
        
        if "Yahoo" in data_mode:
            st.subheader("Sélection des actifs")
            
            # Actifs prédéfinis
            preset_portfolios = {
                "CAC 40 - Blue Chips": ["MC.PA", "TTE.PA", "SAN.PA", "OR.PA", "AI.PA"],
                "Tech US": ["AAPL", "MSFT", "GOOGL", "AMZN", "META"],
                "ETF Diversifié": ["SPY", "AGG", "GLD", "VNQ", "EFA"],
                "Personnalisé": []
            }
            
            selected_preset = st.selectbox("Portefeuille prédéfini", list(preset_portfolios.keys()))
            
            if selected_preset == "Personnalisé":
                custom_tickers = st.text_input(
                    "Symboles (séparés par virgule)",
                    "AAPL, MSFT, GOOGL"
                )
                tickers = [t.strip().upper() for t in custom_tickers.split(",")]
            else:
                tickers = preset_portfolios[selected_preset]
                st.write(f"Actifs: {', '.join(tickers)}")
            
            # Période
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Début", datetime.now() - timedelta(days=365*3))
            with col2:
                end_date = st.date_input("Fin", datetime.now())
            
            # Dans la sidebar, section Yahoo Finance, modifiez le bouton "Charger les données" :

            if st.button("📥 Charger les données", type="primary"):
                # Convertir date en datetime
                start_datetime = datetime.combine(start_date, datetime.min.time())
                end_datetime = datetime.combine(end_date, datetime.min.time())
                
                prices = load_market_data(tickers, start_datetime, end_datetime)
                if prices is not None:
                    st.session_state.prices_df = prices
                    st.session_state.returns_df = prices.pct_change().dropna()
                    st.session_state.selected_assets = list(prices.columns)
                    st.success(f"✅ {len(prices)} observations chargées")
        else:
            # Données synthétiques
            st.subheader("Configuration synthétique")
            n_assets = st.slider("Nombre d'actifs", 3, 10, 5)
            n_periods = st.slider("Périodes", 100, 1000, 252)
            
            if st.button("🎲 Générer données", type="primary"):
                np.random.seed(42)
                # Simulation de rendements
                expected_rets = np.random.uniform(0.05, 0.15, n_assets)
                volatilities = np.random.uniform(0.10, 0.35, n_assets)
                
                returns = np.zeros((n_periods, n_assets))
                for i in range(n_assets):
                    returns[:, i] = np.random.normal(
                        expected_rets[i] / 252,
                        volatilities[i] / np.sqrt(252),
                        n_periods
                    )
                
                asset_names = [f"Actif_{i+1}" for i in range(n_assets)]
                st.session_state.returns_df = pd.DataFrame(returns, columns=asset_names)
                st.session_state.selected_assets = asset_names
                st.success(f"✅ Données générées: {n_assets} actifs, {n_periods} périodes")
        
        st.divider()
        
        # Paramètres d'optimisation
        st.subheader("📊 Paramètres d'optimisation")
        
        risk_free_rate = st.number_input(
            "Taux sans risque (r_f) %",
            min_value=0.0, max_value=10.0, value=2.0, step=0.1
        ) / 100
        
        allow_short = st.checkbox("Autoriser les ventes à découvert", value=False)
        
        if allow_short:
            min_weight = st.slider("Poids minimum", -0.5, 0.0, -0.1)
        else:
            min_weight = 0.0
        
        max_weight = st.slider("Poids maximum par actif", 0.2, 1.0, 0.5)
        
        num_frontier_points = st.slider("Points frontière", 20, 100, 50)
    
    # Onglets principaux
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Analyse des Données",
        "🎯 Frontière Efficiente", 
        "💼 Portefeuilles Optimaux",
        "⚠️ Analyse des Risques",
        "📚 Théorie"
    ])
    
    # Tab 1: Analyse des données
    with tab1:
        if st.session_state.returns_df is not None:
            returns_df = st.session_state.returns_df
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📈 Statistiques Descriptives")
                
                # Calcul des statistiques annualisées
                stats_df = pd.DataFrame({
                    'Rendement annualisé (%)': returns_df.mean() * 252 * 100,
                    'Volatilité annualisée (%)': returns_df.std() * np.sqrt(252) * 100,
                    'Sharpe (r_f=2%)': (returns_df.mean() * 252 - 0.02) / (returns_df.std() * np.sqrt(252)),
                    'Skewness': returns_df.skew(),
                    'Kurtosis': returns_df.kurtosis()
                }).round(3)
                
                st.dataframe(stats_df, width="stretch")
            
            with col2:
                st.subheader("🔗 Matrice de Corrélation")
                
                corr_matrix = returns_df.corr()
                
                fig = px.imshow(
                    corr_matrix,
                    labels=dict(color="Corrélation"),
                    color_continuous_scale='RdBu_r',
                    zmin=-1, zmax=1
                )
                fig.update_layout(
                    template='plotly_dark',
                    paper_bgcolor='#16213e',
                )
                st.plotly_chart(
    fig,
    config={"responsive": True}
)
            
            # Distribution des rendements
            st.subheader("📊 Distribution des Rendements")
            
            selected_asset = st.selectbox("Sélectionner un actif", st.session_state.selected_assets)
            
            fig = make_subplots(rows=1, cols=2, subplot_titles=['Histogramme', 'Série temporelle'])
            
            fig.add_trace(
                go.Histogram(x=returns_df[selected_asset] * 100, nbinsx=50, marker_color='#e94560'),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(y=returns_df[selected_asset].cumsum() * 100, mode='lines', 
                          line=dict(color='#64ffda')),
                row=1, col=2
            )
            
            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor='#16213e',
                plot_bgcolor='#1a1a2e',
                showlegend=False
            )
            st.plotly_chart(
    fig,
    config={"responsive": True}
)
        
        else:
            st.info("👆 Veuillez charger des données dans la barre latérale pour commencer.")
    
    # Tab 2: Frontière Efficiente
    with tab2:
        if st.session_state.returns_df is not None:
            returns_df = st.session_state.returns_df
            
            if st.button("🚀 Calculer la Frontière Efficiente", type="primary"):
                with st.spinner("Optimisation en cours..."):
                    returns_array = returns_df.values
                    expected_returns = calculate_expected_returns(returns_array) * 252
                    cov_matrix = calculate_covariance_matrix(returns_array) * 252
                    
                    frontier = compute_efficient_frontier(
                        expected_returns,
                        cov_matrix,
                        risk_free_rate=risk_free_rate,
                        num_points=num_frontier_points,
                        allow_short_selling=allow_short,
                        min_weight=min_weight,
                        max_weight=max_weight
                    )
                    
                    st.session_state.frontier = frontier
                    st.success("✅ Frontière efficiente calculée!")
            
            if st.session_state.frontier is not None:
                frontier = st.session_state.frontier
                
                # Graphique principal
                fig = create_efficient_frontier_plot(frontier, risk_free_rate)
                st.plotly_chart(
    fig,
    config={"responsive": True}
)
                
                # Métriques clés
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "Portefeuilles sur la frontière",
                        len(frontier.points)
                    )
                
                with col2:
                    st.metric(
                        "Min Variance - Risque",
                        f"{frontier.min_variance_portfolio.volatility * 100:.2f}%"
                    )
                
                with col3:
                    st.metric(
                        "Max Sharpe",
                        f"{frontier.max_sharpe_portfolio.sharpe_ratio:.3f}"
                    )
        else:
            st.info("👆 Veuillez charger des données pour calculer la frontière efficiente.")
    
    # Tab 3: Portefeuilles Optimaux
    with tab3:
        if st.session_state.frontier is not None:
            frontier = st.session_state.frontier
            assets = st.session_state.selected_assets
            
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
                | VaR 95% | **{calculate_var(min_var.expected_return, min_var.volatility) * 100:.2f}%** |
                """)
                
                fig = create_weights_plot(min_var.weights, assets, "Allocations - Min Variance")
                st.plotly_chart(
    fig,
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
                | VaR 95% | **{calculate_var(max_sharpe.expected_return, max_sharpe.volatility) * 100:.2f}%** |
                """)
                
                fig = create_weights_plot(max_sharpe.weights, assets, "Allocations - Max Sharpe")
                st.plotly_chart(
    fig,
    config={"responsive": True}
)
            
            # Comparaison
            st.subheader("📊 Comparaison des Portefeuilles")
            
            comparison_df = pd.DataFrame({
                'Min Variance': min_var.weights * 100,
                'Max Sharpe': max_sharpe.weights * 100
            }, index=assets)
            
            st.dataframe(comparison_df.style.format("{:.1f}%"), width="stretch")
        
        else:
            st.info("👆 Calculez d'abord la frontière efficiente dans l'onglet précédent.")
    
    # Tab 4: Analyse des Risques
    with tab4:
        if st.session_state.frontier is not None:
            frontier = st.session_state.frontier
            
            st.subheader("⚠️ Mesures de Risque")
            
            # Sélection du portefeuille
            portfolio_choice = st.radio(
                "Portefeuille à analyser",
                ["Variance Minimale", "Max Sharpe"],
                horizontal=True
            )
            
            if portfolio_choice == "Variance Minimale":
                portfolio = frontier.min_variance_portfolio
            else:
                portfolio = frontier.max_sharpe_portfolio
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                var_95 = calculate_var(portfolio.expected_return, portfolio.volatility, 0.95)
                st.metric("VaR 95% (1 jour)", f"{var_95 * 100:.2f}%")
                
            with col2:
                var_99 = calculate_var(portfolio.expected_return, portfolio.volatility, 0.99)
                st.metric("VaR 99% (1 jour)", f"{var_99 * 100:.2f}%")
            
            with col3:
                cvar = calculate_cvar(portfolio.expected_return, portfolio.volatility, 0.95)
                st.metric("CVaR 95%", f"{cvar * 100:.2f}%")
            
            # Explication
            st.markdown("""
            ---
            **Interprétation:**
            
            - **VaR 95%**: Avec 95% de confiance, la perte journalière ne dépassera pas cette valeur.
            - **VaR 99%**: Niveau de confiance plus élevé, donc perte potentielle plus importante.
            - **CVaR (Expected Shortfall)**: Perte moyenne attendue au-delà de la VaR.
            
            **Formule VaR paramétrique:**
            """)
            
            st.latex(r"VaR_\alpha = -(\mu_p - z_\alpha \cdot \sigma_p)")
        
        else:
            st.info("👆 Calculez d'abord la frontière efficiente.")
    
    # Tab 5: Théorie
    with tab5:
        st.subheader("📚 Théorie Moderne du Portefeuille - Markowitz")
        
        st.markdown("""
        Cette application implémente le modèle de Markowitz (1952), fondement de la théorie 
        moderne du portefeuille. Voici les concepts clés abordés :
        """)
        
        with st.expander("1-2. Rendement et Risque"):
            st.latex(r"\mu_i = E[R_i] = \frac{1}{T}\sum_{t=1}^{T} R_{i,t}")
            st.latex(r"\sigma_i^2 = Var(R_i) = E[(R_i - \mu_i)^2]")
            st.markdown("Le rendement espéré μ et la volatilité σ caractérisent chaque actif.")
        
        with st.expander("3-4. Portefeuille et Matrice de Covariance"):
            st.latex(r"\mu_p = \sum_{i=1}^{n} w_i \mu_i = \mathbf{w}'\boldsymbol{\mu}")
            st.latex(r"\sigma_p^2 = \sum_{i=1}^{n}\sum_{j=1}^{n} w_i w_j \sigma_{ij} = \mathbf{w}'\boldsymbol{\Sigma}\mathbf{w}")
            st.markdown("Le risque dépend des covariances, pas seulement des variances individuelles.")
        
        with st.expander("7-8. Problème d'Optimisation"):
            st.latex(r"\min_{\mathbf{w}} \mathbf{w}'\boldsymbol{\Sigma}\mathbf{w}")
            st.latex(r"\text{s.t.} \quad \mathbf{w}'\boldsymbol{\mu} = r^*, \quad \sum_i w_i = 1")
            st.markdown("""
            Le problème de Markowitz minimise la variance pour un rendement cible donné.
            C'est un problème d'optimisation quadratique convexe.
            """)
        
        with st.expander("9-10. Ratio de Sharpe et Portefeuille Tangent"):
            st.latex(r"S = \frac{\mu_p - r_f}{\sigma_p}")
            st.markdown("""
            Le **ratio de Sharpe** mesure le rendement ajusté au risque par rapport au taux sans risque.
            
            Le **portefeuille tangent** maximise ce ratio et représente le point de contact entre 
            la frontière efficiente et la Capital Market Line (CML).
            """)
        
        with st.expander("11. Frontière Efficiente"):
            st.markdown("""
            La **frontière efficiente** est l'ensemble des portefeuilles qui:
            - Maximisent le rendement pour un niveau de risque donné
            - Minimisent le risque pour un niveau de rendement donné
            
            Elle forme une hyperbole dans l'espace μ-σ.
            """)
        
        with st.expander("12. Mesures de Risque Avancées"):
            st.latex(r"VaR_\alpha = -(\mu_p - z_\alpha \sigma_p)")
            st.latex(r"CVaR_\alpha = -\mu_p + \sigma_p \frac{\phi(z_\alpha)}{1-\alpha}")
            st.markdown("""
            - **VaR**: Perte maximale au seuil de confiance α
            - **CVaR**: Perte moyenne au-delà de la VaR (Expected Shortfall)
            """)
        
        st.markdown("""
        ---
        **Référence:** Document `prog_finance.pdf` - Programmation pour la Finance.        """)


if __name__ == "__main__":
    main()
