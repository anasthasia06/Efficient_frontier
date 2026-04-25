#!/usr/bin/env bash
# Lance la stack complète : Streamlit + monitoring (Grafana, Prometheus, Loki, cAdvisor)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "Démarrage de la stack complète..."
docker compose up -d --build

GRAFANA_PORT="${GRAFANA_HOST_PORT:-3010}"
echo "Services disponibles :"
echo "  Streamlit   → http://localhost:${STREAMLIT_SERVER_PORT:-8501}"
echo "  Grafana     → http://localhost:${GRAFANA_PORT}  (admin / ${GRAFANA_ADMIN_PASSWORD:-admin})"
echo "  Prometheus  → http://localhost:9091"
echo "  cAdvisor    → http://localhost:8088"
