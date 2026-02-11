# 📱 Portfolio Optimizer - Application Mobile

Application React Native / Expo pour l'optimisation de portefeuille.

## 🚀 Démarrage

### Prérequis

- Node.js 18+
- npm ou yarn
- [Expo Go](https://expo.dev/client) sur votre téléphone

### Installation

```bash
# Installer les dépendances
npm install

# Lancer le serveur de développement
npx expo start
```

### Avec Docker

```bash
# Depuis la racine du projet
docker-compose up mobile
```

## ⚙️ Lancement via VS Code (Tâches)

Vous pouvez démarrer cette application directement depuis VS Code via la palette de commandes (`Ctrl+Shift+P` → `Tasks: Run Task`).

- `Docker: Build All` : construit toutes les images Docker du projet
- `Docker: Start All` : démarre les services (incluant Mobile) en conteneurs
- `Docker: Stop All` : arrête tous les services
- `Mobile: Start Expo` : lance Expo en local (hors Docker) dans `apps/mobile`

Accès rapide:
- Expo DevTools: http://localhost:19002
- Metro bundler: http://localhost:8081

Pour les détails complets Docker Compose (services, ports, commandes), voir la section "Lancement des Versions (Docker Compose)" du README racine : [Efficient_frontier/README.md](Efficient_frontier/README.md)


## 📁 Structure

```
app/
├── (auth)/           # Écrans d'authentification
│   ├── _layout.tsx
│   └── login.tsx
├── (tabs)/           # Onglets principaux
│   ├── _layout.tsx
│   ├── index.tsx     # Dashboard
│   ├── optimize.tsx  # Optimisation Markowitz
│   ├── strategy.tsx  # Stratégies
│   └── profile.tsx   # Profil utilisateur
└── _layout.tsx       # Layout racine

src/
├── components/       # Composants réutilisables
├── services/         # Logique métier
│   └── optimization.ts
├── store/           # État global (Zustand)
│   └── index.ts
└── types/           # Types TypeScript
    └── portfolio.ts
```

## 🎨 Design

- Thème sombre moderne
- Couleurs : `#1a1a2e`, `#16213e`, `#e94560`, `#64ffda`
- Charts avec `react-native-chart-kit`

## 📱 Compte de démonstration

```
Email: demo@portfolio.com
Mot de passe: demo123
```
