#!/usr/bin/Library/Frameworks/Python.framework/Versions/3.12/bin/python3
"""
export-pdf.py — Exporta portfolio.html a PDF automáticamente.

Requisitos (una sola vez):
    pip install playwright
    playwright install chromium

Uso directo:
    python3 export-pdf.py

Uso desde export-pdf.sh:
    ./export-pdf.sh
"""

import subprocess
import sys
import time
import os
import re
import base64
import struct
import tempfile
from pathlib import Path

PORT = 8788  # puerto separado del servidor interactivo del build.sh

MIME = {
    ".jpg":  "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png":  "image/png",
    ".gif":  "image/gif",
    ".webp": "image/webp",
    ".svg":  "image/svg+xml",
}


def strip_jpeg_icc(data: bytes) -> bytes:
    """Elimina marcadores APP2 con perfil ICC de un JPEG."""
    out = bytearray(data[:2])  # SOI
    i = 2
    while i < len(data) - 1:
        if data[i] != 0xFF:
            out.extend(data[i:])
            break
        marker = data[i + 1]
        # Marcadores sin longitud
        if marker in (0xD8, 0xD9, 0x01) or (0xD0 <= marker <= 0xD7):
            out.extend(data[i:i + 2])
            i += 2
            continue
        if i + 4 > len(data):
            out.extend(data[i:])
            break
        seg_len = struct.unpack(">H", data[i + 2:i + 4])[0]
        seg_end = i + 2 + seg_len
        # APP2 con perfil ICC → omitir
        if marker == 0xE2 and data[i + 4:i + 16] == b"ICC_PROFILE\x00":
            i = seg_end
            continue
        out.extend(data[i:seg_end])
        i = seg_end
    return bytes(out)


def to_data_uri(path: Path) -> str:
    mime = MIME.get(path.suffix.lower(), "image/jpeg")
    raw = path.read_bytes()
    if path.suffix.lower() in (".jpg", ".jpeg"):
        raw = strip_jpeg_icc(raw)
    data = base64.b64encode(raw).decode()
    return f"data:{mime};base64,{data}"


def embed_images(html: str, base_dir: Path) -> str:
    """Convierte todas las referencias a imágenes en data URIs inline."""

    def replace_url(m):
        raw = m.group(1).strip("'\"")
        if raw.startswith(("http", "data:", "//")):
            return m.group(0)
        # Normaliza ./images/foo.jpg → images/foo.jpg
        clean = raw.lstrip("./")
        img_path = base_dir / clean
        if img_path.exists():
            return f"url('{to_data_uri(img_path)}')"
        return m.group(0)

    def replace_src(m):
        src = m.group(1)
        if src.startswith(("http", "data:", "//")):
            return m.group(0)
        clean = src.lstrip("./")
        img_path = base_dir / clean
        if img_path.exists():
            return f'src="{to_data_uri(img_path)}"'
        return m.group(0)

    html = re.sub(r"url\(([^)]+)\)", replace_url, html)
    html = re.sub(r'src="([^"]+)"', replace_src, html)
    return html


def main():
    html_file = "portfolio.html"
    output    = "portfolio.pdf"
    base_dir  = Path(os.getcwd())

    if not os.path.exists(html_file):
        print(f"✗ No se encontró {html_file}. Ejecuta ./build.sh primero.")
        sys.exit(1)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("✗ Playwright no está instalado.")
        print("  Instálalo con:")
        print("    pip install playwright")
        print("    playwright install chromium")
        sys.exit(1)

    # Pre-procesa el HTML incrustando todas las imágenes como data URIs
    print("→ Incrustando imágenes como data URIs...")
    raw_html = Path(html_file).read_text(encoding="utf-8")
    embedded_html = embed_images(raw_html, base_dir)

    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".html", dir=base_dir,
        prefix="_export_tmp_", delete=False, encoding="utf-8"
    )
    tmp.write(embedded_html)
    tmp.close()
    tmp_name = Path(tmp.name).name

    # Levanta un servidor HTTP temporal (paged.js requiere HTTP, no file://)
    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(PORT)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(0.8)

    try:
        url = f"http://localhost:{PORT}/{tmp_name}"
        print(f"→ Renderizando con paged.js ...")

        with sync_playwright() as p:
            browser = p.chromium.launch(
                args=["--force-color-profile=srgb"]
            )
            page = browser.new_page()
            page.goto(url, wait_until="networkidle")

            # Espera a que paged.js termine de paginar
            page.wait_for_selector(".pagedjs_page", timeout=30000)
            page.wait_for_timeout(2500)  # margen extra para renders complejos

            # Convierte background-image inline en <img> reales para que
            # Chromium los embeba como datos rasterizados en el PDF.
            page.evaluate("""() => {
                document.querySelectorAll('[style]').forEach(el => {
                    const bg = el.style.backgroundImage;
                    if (!bg || !bg.startsWith('url(')) return;
                    const url = bg.slice(4, -1).replace(/['"]/g, '');
                    const img = document.createElement('img');
                    img.src = url;
                    img.style.cssText = [
                        'position:absolute', 'inset:0', 'width:100%',
                        'height:100%', 'object-fit:cover', 'z-index:0',
                        'display:block'
                    ].join(';');
                    el.style.backgroundImage = '';
                    el.insertBefore(img, el.firstChild);
                });
            }""")
            page.wait_for_timeout(500)  # espera a que carguen los imgs

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
        os.unlink(tmp.name)


if __name__ == "__main__":
    main()

