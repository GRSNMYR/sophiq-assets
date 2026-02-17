# WhatsApp Banners - Generador de imágenes para compartir

Scripts Python para generar banners optimizados para WhatsApp a partir de fotos hero de propiedades.

## Contenido

| Archivo | Descripcion |
|---------|-------------|
| `generate_banners.py` | 3 opciones de banner landscape (1200x630) |
| `generate_simple.py` | Banner cuadrado simplificado (1080x1080) |
| `hero_original.jpg` | Foto hero original de la propiedad |
| `serena_whatsapp.jpg` | Banner generado (cuadrado, preview abajo) |

## Opciones de diseño

### `generate_banners.py` — 3 variantes (1200x630)

| Opcion | Estilo | Descripcion |
|--------|--------|-------------|
| 1 | Elegante Gradient | Foto completa + gradiente oscuro inferior + texto blanco con dorado |
| 2 | Premium Split | Imagen izquierda (60%) + panel oscuro derecho con datos |
| 3 | Bold Cinematic | Foto completa + franja horizontal semi-transparente estilo cine |

### `generate_simple.py` — 1 variante (1080x1080)

Formato cuadrado con gradiente inferior fuerte. Texto grande optimizado para preview en movil.

## Requisitos

```bash
pip install Pillow
```

Fuentes del sistema (macOS):
- Didot (titulos)
- Avenir Next (cuerpo)

Logo blanco: `../logos/sophiq-logo-white.png`

## Uso

```bash
# Generar las 3 opciones landscape
python generate_banners.py

# Generar banner cuadrado
python generate_simple.py
```

## Paleta

| Color | Hex | Uso |
|-------|-----|-----|
| Dark | `rgb(20, 25, 30)` | Fondos y gradientes |
| Gold | `rgb(198, 169, 120)` | Acentos, separadores, etiquetas |
| White | `rgb(255, 255, 255)` | Textos principales |
| Cream | `rgb(245, 240, 232)` | Textos secundarios |

## Adaptacion a otras propiedades

Para usar con otra propiedad:
1. Reemplazar `hero_original.jpg` con la nueva foto hero
2. Editar en cada script: nombre, ubicacion, precio, superficie, precio/m2, y features
