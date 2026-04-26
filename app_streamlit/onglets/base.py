from __future__ import annotations

from abc import ABC, abstractmethod

from app_streamlit.state import AppState, OptimizationConfig


class Page(ABC):
    """Base class pour les pages/onglets Streamlit."""

    name: str = ""

    @abstractmethod
    def render(self, state: AppState, config: OptimizationConfig) -> None:
        """Rend le contenu de la page."""
        raise NotImplementedError
