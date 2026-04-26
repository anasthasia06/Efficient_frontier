#!/bin/bash
# Lance le conteneur streamlit en réutilisant l'image existante
cd "$(dirname "$0")/.."
docker compose up streamlit
