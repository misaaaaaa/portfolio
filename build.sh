#!/usr/bin/env bash
# ============================================================
# build.sh — Compila el HTML y abre Chrome para previsualizar
#
# Requisito: pandoc instalado
#   macOS:  brew install pandoc
#   Linux:  sudo apt install pandoc
#   Win:    https://pandoc.org/installing.html
#
# Para exportar a PDF automáticamente, usa:
#   ./export-pdf.sh
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

# paged.js necesita HTTP para leer el CSS (file:// bloquea el XHR en Chrome).
PORT=8787
echo "→ Iniciando servidor local en http://localhost:$PORT/$OUTPUT ..."
python3 -m http.server "$PORT" &
SERVER_PID=$!

sleep 0.5
open -a "Google Chrome" "http://localhost:$PORT/$OUTPUT"

echo ""
echo "Próximos pasos:"
echo "  1. Espera a que paged.js termine de paginar (barra de progreso arriba)"
echo "  2. Cmd+P → Guardar como PDF"
echo "  3. En el diálogo de impresión:"
echo "     - Papel: A4 / Horizontal"
echo "     - Márgenes: Ninguno"
echo "     - Activar: Gráficos de fondo"
echo ""
echo "Presiona Enter para detener el servidor cuando termines..."
read -r
kill "$SERVER_PID" 2>/dev/null
echo "✓ Servidor detenido."
