from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List, Any

import pandas as pd
import streamlit as st


@dataclass
class AppState:
    """Encapsule l'état de l'application pour éviter l'usage direct et dispersé de st.session_state."""
    prices_df: Optional[pd.DataFrame] = None
    returns_df: Optional[pd.DataFrame] = None
    frontier: Optional[Any] = None
    selected_assets: List[str] = field(default_factory=list)
    frontier_assets: List[str] = field(default_factory=list)

    @classmethod
    def load_from_session(cls) -> "AppState":
        """Crée un AppState depuis st.session_state."""
        state = cls()
        state.prices_df = st.session_state.get("prices_df")
        state.returns_df = st.session_state.get("returns_df")
        state.frontier = st.session_state.get("frontier")
        state.selected_assets = st.session_state.get("selected_assets", [])
        state.frontier_assets = st.session_state.get("frontier_assets", [])
        return state

    def sync_to_session(self) -> None:
        """Synchronise l'état local vers st.session_state."""
        st.session_state.prices_df = self.prices_df
        st.session_state.returns_df = self.returns_df
        st.session_state.frontier = self.frontier
        st.session_state.selected_assets = self.selected_assets
        st.session_state.frontier_assets = self.frontier_assets


@dataclass
class OptimizationConfig:
    """Paramètres d'optimisation centralisés."""
    risk_free_rate: float = 0.02
    allow_short: bool = False
    min_weight: float = 0.0
    max_weight: float = 0.5
    num_frontier_points: int = 50
    theme: str = "dark"  # "dark" ou "light"
