# Portfolio
**Markdown → paged.js → PDF**  
Formato: A4 horizontal (297 × 210 mm) · Tema editorial oscuro

---

## Stack

| Herramienta | Rol |
|-------------|-----|
| **Markdown** | Contenido |
| **Pandoc** | Convierte `.md` → `.html` |
| **paged.js** | Pagina el HTML en el navegador |
| **CSS Paged Media** | Controla el layout de impresión |

---

## Estructura

```
portfolio/
├── content.md        ← Edita aquí tu contenido
├── style.css         ← Diseño y tipografía
├── template.html     ← Plantilla HTML para Pandoc (no tocar)
├── build.sh          ← Script de compilación
└── images/
    └── ...           ← Tus imágenes aquí
```

---

## Instalación

```bash
# macOS
brew install pandoc

# Ubuntu / Debian
sudo apt install pandoc

# Windows — descargar desde:
# https://pandoc.org/installing.html
```

---

## Uso

```bash
chmod +x build.sh
./build.sh
```

Luego abre `portfolio.html` en **Google Chrome**:

1. Espera a que paged.js termine de paginar
2. `Cmd+P` → Guardar como PDF
3. Configurar:
   - Papel: **A4** · Orientación: **Horizontal**
   - Márgenes: **Ninguno**
   - ✅ Activar **Gráficos de fondo**

---

## Secciones disponibles

Cada sección se escribe en `content.md` usando `:::` con una clase. Los comentarios en el propio `content.md` explican cada campo.

### Portada

```markdown
::: {.cover}
# Título del portafolio {.cover-title}

::: {.cover-meta}
[Nombre Artista]{.artist-name}

[https://tu-sitio.com](https://tu-sitio.com){.url}
:::
:::
```

La imagen de fondo se define en `style.css` → `.cover { background-image: ... }`.

---

### Biografía

Admite hasta 3 párrafos dentro de `.bio-body`.

```markdown
::: {.bio}
## Biografía

::: {.bio-body}
Párrafo uno...

Párrafo dos...

Párrafo tres...
:::

:::
```

---

### Statement

La columna izquierda contiene la etiqueta y una imagen vertical opcional.  
Para omitir la imagen, elimina el bloque `.statement-image` completo.

```markdown
::: {.statement}
::: {.statement-left}
## Statement

::: {.statement-image}
![](./images/foto-vertical.jpg)
:::
:::

::: {.statement-body}
Tu texto aquí...
:::
:::
```

---

### Proyecto

Usa `{.project}` para imagen a la izquierda o `{.project .project-right}` para imagen a la derecha.  
El texto alternativo de la imagen aparece como crédito fotográfico superpuesto.

```markdown
::: {.project}
::: {.project-image}
![Crédito fotográfico](./images/foto.jpg)
:::

::: {.project-text}
[01]{.project-number}

## Título de la obra

[Instalación]{.project-subtitle}
[Circuitos, parlantes, madera]{.project-materials}

Descripción de la obra...

[Técnica / Año — Ver proyecto →](https://url.com)
:::
:::
```

Campos opcionales que pueden omitirse: `.project-materials`.

---

### Página imagen completa

El texto alternativo aparece como crédito en la esquina inferior derecha.

```markdown
::: {.fullpage}
![Título, año. Foto: Nombre Apellido](./images/foto.jpg)
:::
```

---

## Colores

```css
:root {
  --bg:       #0d0d0d;   /* Fondo general */
  --text:     #e2ddd5;   /* Texto principal */
  --text-dim: #5c5956;   /* Texto secundario */
  --accent:   #a0a0a0;   /* Gris claro (títulos, enlaces) */
  --border:   #1c1c1c;   /* Líneas separadoras */
}
```

## Tipografía

- **IBM Plex Mono** — cuerpo de texto, títulos de proyectos, descripciones
- **Cormorant** — número de proyecto de fondo, etiqueta BIOGRAFÍA
- **Jost** — etiqueta STATEMENT

Las fuentes se cargan desde Google Fonts en `template.html`.

---

## Notas

- paged.js funciona mejor en **Chrome** o **Chromium**
- Si las imágenes no cargan, verifica que estén en `images/`

---

## Créditos

Diseñado y desarrollado por [Matías Serrano Acevedo](https://misaa.cc).  
Estructura, layout y CSS generados en colaboración con **GitHub Copilot** (Claude Sonnet 4.6), abril 2026.
