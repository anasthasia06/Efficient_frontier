from __future__ import annotations

import streamlit as st
from datetime import datetime, timedelta
from typing import List

from state import AppState, OptimizationConfig
from onglets.data_analysis import DataAnalysisPage
from onglets.frontier import FrontierPage
from onglets.optimal import OptimalPortfoliosPage
from onglets.risk import RiskAnalysisPage
from onglets.theory import TheoryPage
from services import MarketDataService, SyntheticDataService


class PortfolioOptimizerApp:
    """Point d'entrée orienté objet. Orchestration de l'état, de la configuration et des pages.

    Cette classe est un squelette pour migrer progressivement la logique existante
    de app.py vers une structure OOP sans casser l'interface actuelle.
    """

    def __init__(self) -> None:
        self.state = AppState.load_from_session()
        self.config = OptimizationConfig()
        self.pages = [
            DataAnalysisPage(),
            FrontierPage(),
            OptimalPortfoliosPage(),
            RiskAnalysisPage(),
            TheoryPage(),
        ]
        self.market_service = MarketDataService()
        self.synthetic_service = SyntheticDataService()

    def _inject_css(self) -> None:
        try:
            with open("assets/styles.css", "r", encoding="utf-8") as f:
                css = f.read()
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
        except Exception:
            # Fallback minimal si le fichier n'est pas accessible
            st.markdown("<style>.main-header{font-size:2rem;font-weight:700;text-align:center}</style>", unsafe_allow_html=True)

    def render_sidebar(self) -> None:
        with st.sidebar:
            st.header("⚙️ Données & Paramètres (OOP)")

            # Sélecteur de thème
            self.config.theme = st.radio("Thème", ["Sombre", "Clair"], index=0)
            # Normaliser en valeurs internes
            self.config.theme = "dark" if self.config.theme == "Sombre" else "light"

            # Source des données
            data_mode = st.radio("Source des données", ["Données de marché (Yahoo Finance)", "Données synthétiques (démo)"])

            if "Yahoo" in data_mode:
                st.subheader("Sélection des actifs")
                preset_portfolios = {
                    "CAC 40 - Blue Chips": ["MC.PA", "TTE.PA", "SAN.PA", "OR.PA", "AI.PA"],
                    "Tech US": ["AAPL", "MSFT", "GOOGL", "AMZN", "META"],
                    "ETF Diversifié": ["SPY", "AGG", "GLD", "VNQ", "EFA"],
                    "Personnalisé": [],
                }
                selected_preset = st.selectbox("Portefeuille prédéfini", list(preset_portfolios.keys()))
                if selected_preset == "Personnalisé":
                    custom_tickers = st.text_input("Symboles (séparés par virgule)", "AAPL, MSFT, GOOGL")
                    tickers: List[str] = [t.strip().upper() for t in custom_tickers.split(",")]
                else:
                    tickers = preset_portfolios[selected_preset]
                    st.write(f"Actifs: {', '.join(tickers)}")

                col1, col2 = st.columns(2)
                with col1:
                    start_date = st.date_input("Début", datetime.now() - timedelta(days=365 * 3))
                with col2:
                    end_date = st.date_input("Fin", datetime.now())

                if st.button("📥 Charger les données (OOP)", type="primary"):
                    start_dt = datetime.combine(start_date, datetime.min.time())
                    end_dt = datetime.combine(end_date, datetime.min.time())
                    prices = self.market_service.load_market_data(tickers, start_dt, end_dt)
                    if prices is not None:
                        self.state.prices_df = prices
                        self.state.returns_df = prices.pct_change().dropna()
                        self.state.selected_assets = list(prices.columns)
                        st.success(f"✅ {len(prices)} observations chargées")
            else:
                st.subheader("Configuration synthétique")
                n_assets = st.slider("Nombre d'actifs", 3, 10, 5)
                n_periods = st.slider("Périodes", 100, 1000, 252)
                if st.button("🎲 Générer données (OOP)", type="primary"):
                    df = self.synthetic_service.generate(n_assets, n_periods, seed=42)
                    self.state.returns_df = df
                    self.state.selected_assets = list(df.columns)
                    st.success(f"✅ Données générées: {n_assets} actifs, {n_periods} périodes")

            st.divider()

            # Paramètres d'optimisation
            st.subheader("📊 Paramètres d'optimisation")
            self.config.risk_free_rate = (
                st.number_input("Taux sans risque (r_f) %", min_value=0.0, max_value=10.0, value=2.0, step=0.1) / 100
            )
            self.config.allow_short = st.checkbox("Autoriser les ventes à découvert", value=False)
            if self.config.allow_short:
                self.config.min_weight = st.slider("Poids minimum", -0.5, 0.0, -0.1)
            else:
                self.config.min_weight = 0.0
            self.config.max_weight = st.slider("Poids maximum par actif", 0.2, 1.0, 0.5)
            self.config.num_frontier_points = st.slider("Points frontière", 20, 100, 50)

    def render_tabs(self) -> None:
        tab_labels = [p.name for p in self.pages]
        tabs = st.tabs(tab_labels, width="stretch")
        for t, p in zip(tabs, self.pages):
            with t:
                p.render(self.state, self.config)

    def run(self) -> None:
        # Mode pleine largeur pour éviter le centrage par défaut
        st.set_page_config(layout="wide", page_title="Portfolio Optimizer (OOP)", page_icon="🧮")

        # Charger le CSS global
        self._inject_css()

        # D'abord rendre la sidebar pour récupérer le thème choisi
        self.render_sidebar()

        # Appliquer le wrapper et une couleur de fond selon le thème
        theme_class = "theme-dark" if self.config.theme == "dark" else "theme-light"
        st.markdown(f"<div class='{theme_class}'>", unsafe_allow_html=True)

        # Override du fond de page pour clarté/sombre
        if self.config.theme == "dark":
            st.markdown("<style>.stApp{background-color:#16213e}</style>", unsafe_allow_html=True)
        else:
            st.markdown("<style>.stApp{background-color:#ffffff}</style>", unsafe_allow_html=True)

        # En-têtes et contenu
        st.markdown('<p class="main-header">🧮💻 Portfolio Optimizer (OOP)</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Optimisation de Portefeuille - Théorie Moderne de Markowitz</p>', unsafe_allow_html=True)
        self.render_tabs()

        # Fermer le wrapper et synchroniser l'état
        st.markdown("</div>", unsafe_allow_html=True)
        self.state.sync_to_session()


# Lancement standalone
if __name__ == "__main__":
    app = PortfolioOptimizerApp()
    app.run()
