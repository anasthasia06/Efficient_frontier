#!/usr/bin/env bash
# Affiche les logs du service demandé (défaut: streamlit)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

SERVICE="${1:-streamlit}"
docker compose logs -f "$SERVICE"
