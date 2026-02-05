# Dockerfile pour l'application mobile React Native / Expo
# Déploiement du serveur de développement Expo dans un conteneur

FROM node:20-slim

# Métadonnées
LABEL maintainer="Portfolio Optimizer Team"
LABEL description="Application mobile React Native / Expo pour l'optimisation de portefeuille"
LABEL version="1.0.0"

# Variables d'environnement
ENV EXPO_DEVTOOLS_LISTEN_ADDRESS=0.0.0.0
ENV REACT_NATIVE_PACKAGER_HOSTNAME=0.0.0.0
ENV CHOKIDAR_USEPOLLING=true

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    git \
    curl \
    watchman \
    && rm -rf /var/lib/apt/lists/*

# Création du répertoire de travail
WORKDIR /app

# Installation globale d'Expo CLI
RUN npm install -g expo-cli @expo/ngrok

# Copie des fichiers de dépendances
COPY package*.json ./

# Installation des dépendances Node.js
RUN npm install

# Copie du code source
COPY . .

# Exposition des ports
# 8081: Metro bundler
# 19000: Expo Dev Server
# 19001: Expo DevTools
# 19002: Expo DevTools (web)
EXPOSE 8081 19000 19001 19002

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:19000 || exit 1

# Commande de démarrage
CMD ["npx", "expo", "start", "--tunnel"]
