# Versiones inglesas de los heroes de email (SQM-2153)

Tres heroes de la secuencia de Lienzos llevaban copy castellano quemado dentro
del JPG. Estos scripts generan la versión `-en` a partir del original, sin
rehacer la imagen: reconstruyen solo la zona del texto y vuelven a escribirlo.

| Script | Original | Salida | Qué cambia |
| --- | --- | --- | --- |
| `build-madrid-forbes-en.py` | `hero/madrid-forbes-mejor-ciudad.jpg` | `...-en.jpg` | Titular y "FUENTE: FORBES" → "SOURCE: FORBES" |
| `build-opalo-labels-en.py` | `email-banners/opalo-{salon,bano}-render-realidad.jpg` | `...-en.jpg` | Etiqueta REALIDAD → REALITY (RENDER no cambia) |
| `build-quien-es-sophiq-ai-badge-en.py` | `email-banners/quien-es-sophiq-ia-hero.jpg` | `...-en.jpg` | Badge del holograma IA → AI |

## Tipografía

El titular del hero de Forbes es **Playfair Display Bold**. No estaba
identificada en ningún sitio: se dedujo ajustando candidatos contra el original
hasta clavar la métrica. A 72 px con tracking −3 px reproduce "Madrid," en
242×66 px exactos, y las otras dos líneas con menos del 1,5 % de desviación.
El fichero va en `tools/PlayfairDisplay-Bold.ttf` (Google Fonts, OFL) porque
NO es una fuente de marca: la de marca es Suisse Intl, que sí está en `fonts/`.

La línea de fuente y las etiquetas de Ópalo son Suisse Intl (Medium 14 px con
1 px de tracking, y Light 16 px respectivamente), ajustadas también por
métrica contra el original.

## Método

1. Máscara de la tinta del texto castellano y `cv2.inpaint` para reconstruir el
   fondo. En el hero de Forbes la pared es lisa y queda invisible; en Ópalo se
   limita al interior de la propia caja de la etiqueta, así que la foto de
   detrás no se toca.
2. Se vuelve a escribir el texto inglés alineando el borde izquierdo de la
   tinta y la línea base a las coordenadas medidas del original.
3. Cada script termina midiendo la tinta resultante y comparándola con la del
   original, para que un cambio no pase inadvertido.

El badge IA → AI no re-tipografía nada: son las mismas dos letras en otro
orden, así que se extrae la máscara de opacidad de cada glifo y se recomponen
intercambiadas. Se conserva el trazo, el antialias y el brillo originales.

## Requisitos

`python3` con `pillow`, `numpy` y `opencv-python`.

## El informe Knight Frank en inglés (3-sep-2026)

`informes/knight-frank-madrid-2026-en.html` es la traducción del castellano,
con **la misma estructura HTML y el mismo CSS**: un `diff` de solo etiquetas da
cero diferencias y los dos ficheros tienen 267 líneas. Solo cambia el texto, y
las cifras pasan a formato inglés (`+5,0%` → `+5.0%`, `13.000–15.400 €/m²` →
`€13,000–15,400 per m²`, `1 M$` → `US$1 M`, FMI → IMF).

Para re-imprimir el PDF después de tocar el HTML:

```sh
cd informes
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-pdf-header-footer \
  --virtual-time-budget=12000 \
  --print-to-pdf=knight-frank-madrid-2026-en.pdf \
  "file://$PWD/knight-frank-madrid-2026-en.html"
```

Ese comando es el que reproduce el PDF castellano **byte a byte** (180.608 B),
así que sirve de control de que el pipeline es el mismo. Salen 6 páginas A4.

**Revisar siempre las 6 páginas rasterizadas antes de dar el PDF por bueno:**
`.page` lleva `overflow:hidden`, y el inglés suele ocupar más que el castellano,
así que un texto que se pase **se recorta sin avisar**. Verificado página a
página en esta versión.

**Un cambio que NO es traducción, en la página 6.** Dos de los cuatro bullets de
«Lectura Sophiq» estaban escritos para dentro (*"alineado con nuestro público"*,
*"útil para neutralizar objeciones de inversores no residentes"*) y ese PDF lo
recibe el lead. En inglés se han reescrito mirando al comprador: *"the market
you would be buying alongside"* y *"the answer to the question every
non-resident buyer asks first"*. Los datos son los mismos. Si se prefiere
paridad literal con el castellano, se revierte en dos líneas.
