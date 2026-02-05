# Dockerfile pour l'application Streamlit Desktop
# Optimisation de portefeuille avancée

FROM python:3.11-slim

# Métadonnées
LABEL maintainer="Portfolio Optimizer Team"
LABEL description="Application Streamlit pour l'optimisation de portefeuille Markowitz"
LABEL version="1.0.0"

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Création du répertoire de travail
WORKDIR /app

# Copie des fichiers de dépendances
COPY requirements.txt .

# Installation des dépendances Python
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Création du répertoire de configuration Streamlit
RUN mkdir -p /root/.streamlit

# Exposition du port Streamlit
EXPOSE 8501

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Commande de démarrage
ENTRYPOINT ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
