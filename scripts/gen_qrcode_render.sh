#!/bin/bash
# Génère un QR code de l'URL Render et le place dans scripts/qrcode_render.png

set -e

URL="https://efficient-frontier-6c9n.onrender.com"
OUTPUT="$(dirname "$0")/qrcode_render.png"

# Vérifie que qrencode est installé
if ! command -v qrencode &> /dev/null; then
  echo "Erreur : qrencode n'est pas installé. Installez-le avec : sudo apt install qrencode"
  exit 1
fi

qrencode -o "$OUTPUT" -s 10 "$URL"
echo "QR code généré : $OUTPUT"