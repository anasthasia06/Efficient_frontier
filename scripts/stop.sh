#!/usr/bin/env bash
# Arrête tous les services Docker Compose
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "Arrêt de tous les services..."
docker compose down
echo "Services arrêtés."
