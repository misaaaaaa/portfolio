#!/usr/bin/env bash
# ============================================================
# export-pdf.sh — Compila el HTML y exporta el PDF automáticamente
#
# Requisitos: pandoc + playwright instalados
#   macOS:  brew install pandoc
#   pip install playwright && playwright install chromium
# ============================================================

set -e

INPUT="content.md"
OUTPUT="portfolio.html"
TEMPLATE="template.html"

echo "→ Compilando $INPUT..."

pandoc "$INPUT" \
  --template="$TEMPLATE" \
  --from markdown+native_divs \
  --to html5 \
  --standalone \
  --output="$OUTPUT"

echo "✓ Listo: $OUTPUT"
echo ""

/Library/Frameworks/Python.framework/Versions/3.12/bin/python3 export-pdf.py
