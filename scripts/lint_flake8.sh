#!/bin/bash
# Lint le code Python avec flake8 et affiche les erreurs
set -e

# S'assure que flake8 est installé
if ! command -v flake8 &> /dev/null; then
  echo "flake8 n'est pas installé. Installation..."
  uv pip install flake8
fi

echo "Version de flake8 :"
flake8 --version

echo "Lint en cours sur le dossier streamlit..."
#!/bin/bash
# Lint le code Python avec Ruff et affiche les erreurs
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
