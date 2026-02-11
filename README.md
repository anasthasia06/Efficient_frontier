# 📈 Portfolio Optimizer - Démonstrateur Optimisation de Portefeuille

Application complète pour l'optimisation de portefeuille basée sur le **modèle de Markowitz** et les 14 points du document de référence `prog_finance_fr_v2.pdf`.

## 🎯 Objectif

Ce projet propose deux applications complémentaires pour les gestionnaires de portefeuille :

1. **Application Mobile** (React Native / Expo) - Android & iOS
   - Interface simplifiée pour la consultation
   - Calcul de frontière efficiente
   - Définition de stratégies d'investissement
   - Visualisation des allocations

2. **Application Desktop** (Streamlit)
   - Interface avancée pour l'analyse approfondie
   - Données de marché en temps réel (Yahoo Finance)
   - Optimisation paramétrable
   - Mesures de risque avancées (VaR, CVaR)

## 📦 Architecture du Projet

```
Efficient_frontier/
├── apps/
│   ├── mobile/              # Application React Native / Expo
│   │   ├── app/             # Écrans (expo-router)
│   │   ├── src/
│   │   │   ├── components/  # Composants UI
│   │   │   ├── services/    # Logique métier (optimisation)
│   │   │   ├── store/       # État global (Zustand)
│   │   │   └── types/       # Types TypeScript
│   │   ├── Dockerfile
│   │   └── package.json
│   │
│   └── streamlit/           # Application Streamlit
│       ├── core/            # Module d'optimisation Python
│       │   └── optimization.py
│       ├── app.py           # Application principale
│       ├── Dockerfile
│       └── requirements.txt
│
├── Efficient_Frontier_Fr/   # Documentation LaTeX
│   ├── tex/
│   └── build/
│
├── docker-compose.yml       # Orchestration Docker
├── .env.example             # Variables d'environnement
└── README.md
```

## 🚀 Lancement des Versions (Docker Compose)

Les deux applications (Desktop Streamlit et Mobile Expo) sont packagées dans des conteneurs Docker et orchestrées via `docker-compose`. Cela permet un lancement homogène, sans installer Node/Expo ou Python localement.

### Prérequis
- Docker et Docker Compose installés
- Ports disponibles: `8501` (Streamlit), `19000/19001/19002` et `8081` (Expo/Metro)

### Démarrage global
```bash
# Construire toutes les images
docker-compose build

# Démarrer tous les services en arrière-plan
docker-compose up -d

# Vérifier les logs (optionnel)
docker-compose logs -f
```

### Démarrage par application
- Streamlit (Desktop):
```bash
docker-compose up -d streamlit
```
   Accès: http://localhost:8501

- Mobile (Expo):
```bash
docker-compose up -d mobile
```
   Accès: Expo DevTools http://localhost:19002

### Rebuild ciblé
```bash
# Reconstruire et relancer uniquement Streamlit
docker-compose up -d --build streamlit

# Reconstruire et relancer uniquement Mobile
docker-compose up -d --build mobile
```

### Arrêt
```bash
docker-compose down
```

### Notes spécifiques Expo en conteneur
- Le conteneur expose `19000/19001/19002` et `8081`. Assurez-vous que votre appareil (ou émulateur) est joignable sur le même réseau que votre machine.
- En cas de difficultés de connexion depuis un appareil physique, privilégiez un émulateur (Android Emulator / iOS Simulator) ou le mode tunnel d’Expo.

## ⚙️ Lancement via VS Code (Tâches)

Vous pouvez démarrer les versions directement depuis VS Code avec les tâches configurées.

- Ouvrir la palette de commandes: `Ctrl+Shift+P` → `Tasks: Run Task`
- Choisir l’une des tâches:
   - `Docker: Build All` : construit toutes les images
   - `Docker: Start All` : démarre Streamlit et Mobile en conteneurs
   - `Docker: Stop All` : arrête tous les services
   - `Streamlit: Run` : lance Streamlit en local (hors Docker) dans `apps/streamlit`
   - `Mobile: Start Expo` : lance Expo en local (hors Docker) dans `apps/mobile`

Astuce: vous pouvez aussi utiliser le menu Terminal → Run Task… pour retrouver ces commandes.

## 🚀 Démarrage Rapide

### Prérequis

- [Docker](https://www.docker.com/) et Docker Compose
- [Node.js](https://nodejs.org/) v18+ (pour dev mobile local)
- [Python](https://www.python.org/) 3.10+ (pour dev Streamlit local)
- [Expo Go](https://expo.dev/client) sur votre téléphone

### Avec Docker (Recommandé)

```bash
# Cloner le repository
git clone <URL_DU_REPO>
cd Efficient_frontier

# Copier les variables d'environnement
cp .env.example .env

# Lancer les conteneurs
docker-compose up -d

# Accéder aux applications
# - Streamlit : http://localhost:8501
# - Expo DevTools : http://localhost:19002
```

### Développement Local

#### Application Mobile (Expo)

```bash
cd apps/mobile

# Installer les dépendances
npm install

# Lancer Expo
npx expo start

# Scanner le QR code avec Expo Go sur votre téléphone
```

#### Application Streamlit

```bash
cd apps/streamlit

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: .\venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app.py
```

## 📱 Fonctionnalités

### Application Mobile

| Fonctionnalité | Description |
|----------------|-------------|
| **Authentification** | Connexion sécurisée des gestionnaires |
| **Dashboard** | Vue d'ensemble du portefeuille (μ, σ, Sharpe) |
| **Optimisation** | Calcul de la frontière efficiente |
| **Stratégies** | Définition de profils de risque personnalisés |
| **Profil** | Paramètres utilisateur |

### Application Streamlit

| Fonctionnalité | Description |
|----------------|-------------|
| **Données de marché** | Chargement depuis Yahoo Finance |
| **Analyse statistique** | Moments, corrélations, distributions |
| **Frontière efficiente** | Visualisation interactive (Plotly) |
| **Portefeuilles optimaux** | Min Variance, Max Sharpe |
| **Analyse de risque** | VaR, CVaR, mesures avancées |
| **Théorie** | Documentation mathématique intégrée |

## 📐 Théorie Mathématique

L'application implémente les concepts du **modèle de Markowitz** :

### Rendement et Risque du Portefeuille

$$\mu_p = \mathbf{w}'\boldsymbol{\mu} = \sum_{i=1}^{n} w_i \mu_i$$

$$\sigma_p^2 = \mathbf{w}'\boldsymbol{\Sigma}\mathbf{w}$$

### Problème d'Optimisation

$$\min_{\mathbf{w}} \mathbf{w}'\boldsymbol{\Sigma}\mathbf{w}$$

Sous contraintes :
- $\mathbf{w}'\boldsymbol{\mu} = r^*$ (rendement cible)
- $\sum_i w_i = 1$ (budget)
- $w_{min} \leq w_i \leq w_{max}$ (bornes)

### Ratio de Sharpe

$$S = \frac{\mu_p - r_f}{\sigma_p}$$

## 🐳 Commandes Docker

```bash
# Construire les images
docker-compose build

# Démarrer tous les services
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter les services
docker-compose down

# Reconstruire un service spécifique
docker-compose up -d --build streamlit
```

## 👥 Collaboration

### Pour les Collaborateurs Distants

1. **Cloner le repository**
   ```bash
   git clone <URL_DU_REPO>
   ```

2. **Créer une branche de travail**
   ```bash
   git checkout -b feature/ma-fonctionnalite
   ```

3. **Suivre les conventions**
   - Mobile : TypeScript strict, composants fonctionnels
   - Streamlit : Python 3.10+, type hints, docstrings
   - Commits : messages clairs en français ou anglais

4. **Soumettre une Pull Request**
   - Description claire des changements
   - Tests si applicable
   - Screenshots pour les changements UI

### Structure des Branches

```
main                 # Production stable
├── develop          # Intégration
├── feature/*        # Nouvelles fonctionnalités
├── bugfix/*         # Corrections
└── docs/*           # Documentation
```

## 📚 Références

- Document de référence : `Efficient_Frontier_Fr/build/prog_finance_fr_v2.pdf`
- Markowitz, H. (1952). "Portfolio Selection". *Journal of Finance*
- [Expo Documentation](https://docs.expo.dev/)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 📄 Licence

Ce projet est développé dans le cadre du cours "Programmation pour la Finance" - UE Info 2025-2026.

---

**Développé dans le cadre d'une optimisation de portefeuille**