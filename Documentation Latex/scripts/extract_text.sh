#!/usr/bin/env bash
set -euo pipefail
# Simple helper to extract raw text from the source PDF
# Requires: poppler-utils (pdftotext)

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SRC_PDF="${ROOT_DIR}/../prog_finance.pdf"
OUT_TXT="${ROOT_DIR}/data/prog_finance_raw.txt"

if ! command -v pdftotext >/dev/null 2>&1; then
  echo "Erreur: 'pdftotext' introuvable. Installez poppler-utils (ex: sudo apt-get install poppler-utils)." >&2
  exit 1
fi

if [[ ! -f "${SRC_PDF}" ]]; then
  echo "Erreur: PDF source introuvable: ${SRC_PDF}" >&2
  exit 1
fi

mkdir -p "${ROOT_DIR}/data"
pdftotext -layout -enc UTF-8 "${SRC_PDF}" "${OUT_TXT}"
echo "Texte extrait: ${OUT_TXT}"
