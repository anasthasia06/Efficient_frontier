#!/bin/bash
# Lance le conteneur streamlit en réutilisant l'image existante
cd "$(dirname "$0")/.."
fuser -k 8501/tcp
docker compose up streamlit
