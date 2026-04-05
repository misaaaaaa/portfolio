#!/usr/bin/Library/Frameworks/Python.framework/Versions/3.12/bin/python3
"""
export-pdf.py — Exporta portfolio.html a PDF automáticamente.

Requisitos (una sola vez):
    pip install playwright
    playwright install chromium

Uso directo:
    python3 export-pdf.py

Uso desde build.sh:
    ./build.sh --pdf
"""

import subprocess
import sys
import time
import os

PORT = 8788  # puerto separado del servidor interactivo del build.sh


def main():
    html = "portfolio.html"
    output = "portfolio.pdf"

    if not os.path.exists(html):
        print(f"✗ No se encontró {html}. Ejecuta ./build.sh primero.")
        sys.exit(1)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("✗ Playwright no está instalado.")
        print("  Instálalo con:")
        print("    pip install playwright")
        print("    playwright install chromium")
        sys.exit(1)

    # Levanta un servidor HTTP temporal (paged.js requiere HTTP, no file://)
    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(PORT)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(0.8)

    try:
        url = f"http://localhost:{PORT}/{html}"
        print(f"→ Renderizando {url} con paged.js ...")

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, wait_until="networkidle")

            # Espera a que paged.js termine de paginar
            page.wait_for_selector(".pagedjs_page", timeout=30000)
            page.wait_for_timeout(2500)  # margen extra para renders complejos

            page.pdf(
                path=output,
                format="A4",
                landscape=True,
                print_background=True,
                margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            )
            browser.close()

        print(f"✓ PDF generado: {output}")

    finally:
        server.terminate()


if __name__ == "__main__":
    main()
