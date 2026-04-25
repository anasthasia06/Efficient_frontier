#!/usr/bin/env bash
# Lance uniquement le service Streamlit en local
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "Démarrage du service Streamlit..."
docker compose up -d --build streamlit
echo "Streamlit disponible sur http://localhost:${STREAMLIT_SERVER_PORT:-8501}"
