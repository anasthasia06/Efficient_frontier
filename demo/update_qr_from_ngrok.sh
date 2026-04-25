#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_FILE="$ROOT_DIR/demo/qr_code_target.txt"
PNG_FILE="$ROOT_DIR/demo/qr_code.png"
NGROK_API="http://127.0.0.1:4040/api/tunnels"

if ! command -v curl >/dev/null 2>&1; then
  echo "Erreur: curl n'est pas installé." >&2
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "Erreur: python3 n'est pas installé." >&2
  exit 1
fi

if ! curl -fsS "$NGROK_API" >/dev/null 2>&1; then
  echo "Erreur: API ngrok inaccessible sur $NGROK_API" >&2
  echo "Lance d'abord: ngrok http 8080" >&2
  exit 1
fi

HTTPS_URL="$(curl -fsS "$NGROK_API" | python3 -c '
import json,sys
payload=json.load(sys.stdin)
urls=[t.get("public_url","") for t in payload.get("tunnels",[]) if t.get("public_url","").startswith("https://")]
print(urls[0] if urls else "")
')"

if [[ -z "$HTTPS_URL" ]]; then
  echo "Erreur: aucune URL HTTPS ngrok trouvée." >&2
  echo "Vérifie que ngrok est lancé avec: ngrok http 8080" >&2
  exit 1
fi

printf '%s\n' "$HTTPS_URL" > "$TARGET_FILE"
echo "OK: URL QR mise à jour dans $TARGET_FILE"
echo "URL active: $HTTPS_URL"

if command -v qrencode >/dev/null 2>&1; then
  qrencode -o "$PNG_FILE" -s 8 -m 2 "$HTTPS_URL"
  echo "OK: QR code image généré: $PNG_FILE"
else
  echo "Info: qrencode non installé, image QR non générée."
  echo "Installe-le si besoin: sudo apt install qrencode"
fi
