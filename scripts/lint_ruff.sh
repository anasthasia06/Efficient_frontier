#!/bin/bash
# Lint le code Python avec ruff et affiche les erreurs
set -e

# S'assure que ruff est installé
if ! command -v ruff &> /dev/null; then
  echo "ruff n'est pas installé. Installation..."
  uv pip install ruff
fi

echo "Version de ruff :"
ruff --version

echo "Lint en cours sur le dossier app_streamlit..."
ruff check app_streamlit
