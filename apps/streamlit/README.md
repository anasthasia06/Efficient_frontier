# 💻 Portfolio Optimizer - Application Streamlit

Application desktop avancée pour l'optimisation de portefeuille basée sur le modèle de Markowitz.

## 🚀 Démarrage

### Prérequis

- Python 3.10+
- pip

### Installation

```bash
# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: .\venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app.py
```

### Avec Docker

```bash
# Depuis la racine du projet
docker-compose up streamlit

# Accéder à http://localhost:8501
```

## 📁 Structure

```
streamlit/
├── app.py              # Application principale
├── core/               # Module d'optimisation
│   ├── __init__.py
│   └── optimization.py # Algorithmes Markowitz
├── .streamlit/
│   └── config.toml     # Configuration Streamlit
├── Dockerfile
└── requirements.txt
```

## 🎯 Fonctionnalités

### Onglets

1. **Analyse des Données**
   - Statistiques descriptives (μ, σ, Sharpe, Skewness, Kurtosis)
   - Matrice de corrélation
   - Distribution des rendements

2. **Frontière Efficiente**
   - Calcul de la frontière μ-σ
   - Visualisation interactive (Plotly)
   - Capital Market Line

3. **Portefeuilles Optimaux**
   - Variance Minimale
   - Max Sharpe (Tangent)
   - Allocations détaillées

4. **Analyse des Risques**
   - VaR paramétrique (95%, 99%)
   - CVaR / Expected Shortfall

5. **Théorie**
   - Documentation mathématique intégrée
   - Formules LaTeX

## 📊 Sources de Données

- **Yahoo Finance** : Données de marché en temps réel
- **Données synthétiques** : Mode démo pour les tests

## 🧮 Module d'Optimisation

Le module `core/optimization.py` implémente :

- `calculate_expected_returns()` : μ = E[R]
- `calculate_covariance_matrix()` : Σ
- `optimize_min_variance()` : min w'Σw
- `optimize_max_sharpe()` : max (μ-rf)/σ
- `compute_efficient_frontier()` : Frontière complète
- `calculate_var()` : Value at Risk
- `calculate_cvar()` : Conditional VaR
