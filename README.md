# 🧮💻 Portfolio Optimizer - Démo Web

Démonstrateur d’optimisation de portefeuille basé sur **Streamlit** et servi en conteneurs Docker.

## 🎯 Périmètre de la démo

La démo fonctionne uniquement avec :

- une **landing page** statique pour l’entrée via QR code
- l’**application web Streamlit**

## 🗂️ Architecture

```text
Efficient_frontier/
├── apps/
│   └── streamlit/          # Application web Streamlit
├── demo/                   # Landing page QR code
└── docker-compose.yml      # Orchestration Docker
```

## 🐳 Lancement (Docker Compose)

### Prérequis

- Docker et Docker Compose installés
- Ports disponibles :
  - `8080` pour la landing page
  - `8501` pour Streamlit

### Démarrer les services

```bash
docker compose up -d --build
```

### Accès

- Landing page : `http://localhost:8080`
- Streamlit : `http://localhost:8501/app/`

Depuis un smartphone sur le même réseau local :

- Landing page : `http://<IP_PC>:8080`
- Streamlit : `http://<IP_PC>:8501/app/`

## 📱 Démo smartphone via QR code

### 1) Lancer le projet avec Docker Compose

```bash
docker compose up -d --build
```

### 2) Accéder à la landing page

- En local : `http://localhost:8080`
- Sur smartphone (même Wi-Fi) : `http://<IP_PC>:8080`

### 3) Générer le QR code (option tunnel HTTPS recommandée)

Lancer ngrok dans un terminal séparé :

```bash
ngrok http 8080
```

Puis mettre à jour la cible QR et générer l'image :

```bash
bash demo/update_qr_from_ngrok.sh
```

Le script met à jour `demo/qr_code_target.txt` et génère `demo/qr_code.png` si `qrencode` est installé.

### 4) Tester la démo depuis un smartphone

- Ouvrir `demo/qr_code.png` sur le PC
- Scanner le QR code avec le smartphone
- Vérifier le flux : landing HTTPS ngrok → bouton `Tester la démo` → `/app/`

## 📊 Stack Monitoring (Grafana / Prometheus / Loki)

### Démarrer la stack monitoring avec Docker Compose

```bash
docker compose up -d grafana prometheus loki promtail cadvisor
```

### Accéder à Grafana

- Grafana (administration locale) : `http://localhost:3010` (ou la valeur de `GRAFANA_HOST_PORT`)
- Prometheus (administration locale) : `http://localhost:9091`

### Consulter les logs et les métriques

- Dans Grafana, ouvrir le dashboard par défaut **Monitoring Overview**
  - métriques système
  - métriques Docker
  - logs applicatifs
- Pour les logs détaillés, utiliser **Explore** avec la source **Loki**.
- Pour les métriques brutes, utiliser **Explore** avec la source **Prometheus**.

### Dépannage Grafana (dashboard/home)

Si Grafana affiche `Failed to load dashboard` ou `Failed to load home dashboard` :

1. Vérifier l'état des services monitoring :

```bash
docker compose ps
curl -s -o /dev/null -w 'grafana:%{http_code}\n' http://localhost:${GRAFANA_HOST_PORT:-3010}/api/health
curl -s -o /dev/null -w 'prometheus:%{http_code}\n' http://localhost:9091/-/healthy
curl -s -o /dev/null -w 'loki:%{http_code}\n' http://localhost:3100/ready
```

2. Ouvrir directement le dashboard provisionné :

```text
http://localhost:3010/d/monitoring-overview/monitoring-overview
```

3. Si nécessaire, redémarrer uniquement la stack monitoring :

```bash
docker compose up -d grafana prometheus loki promtail cadvisor
```

4. En cas d'erreur persistante côté UI, faire un hard refresh (`Ctrl+F5`) ou se reconnecter à Grafana.

## 🧪 Vérification rapide

```bash
docker compose ps
docker compose logs -f landing
docker compose logs -f streamlit
```

## 🛑 Arrêt

```bash
docker compose down
```
